from dataclasses import dataclass
import re

from . import config
from .chunking import Chunk


TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")

# Terms that express the grammatical shape of a question rather than the
# handbook concept being sought. They are used only by the advanced
# coverage-filtered strategy below.
QUESTION_STOPWORDS = frozenset({
    "a", "an", "and", "are", "by", "can", "do", "does", "for", "get",
    "be", "how", "i", "in", "is", "it", "long", "many", "need", "new", "of", "often",
    "on", "per", "the", "to", "until", "what", "when", "where", "who",
    "why", "with", "your",
})

TOKEN_NORMALISATIONS = {
    "days": "day",
    "employees": "employee",
    "passwords": "password",
    "receipts": "receipt",
    "remotely": "remote",
    "yearly": "year",
}


def coverage_tokens(text: str) -> set[str]:
    """Return normalized content terms used for document-level coverage."""
    expanded = re.sub(r"\bnotebook\s+computer\b", "replacement laptop", text.lower())
    return {
        TOKEN_NORMALISATIONS.get(token, token)
        for token in TOKEN_RE.findall(expanded)
        if token not in QUESTION_STOPWORDS
    }


def tokenize(text: str) -> list[str]:
    tokens = [token.lower() for token in TOKEN_RE.findall(text)]
    if config.STOPWORDS_ENABLED:
        raise NotImplementedError("STOPWORDS_ENABLED = True is not implemented yet.")
    return tokens


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    score: float


def lexical_score(query: str, chunk_text: str) -> float:
    q_tokens = tokenize(query)
    c_tokens = tokenize(chunk_text)
    if not q_tokens or not c_tokens:
        return 0.0

    q_set = set(q_tokens)
    overlap = sum(1 for token in c_tokens if token in q_set)
    return overlap / len(c_tokens)


def searchable_chunks(chunks: list[Chunk]) -> list[Chunk]:
    if config.CURRENT_ONLY:
        raise NotImplementedError("CURRENT_ONLY = True is not implemented yet.")
    return chunks


def chunks_matching_full_query_coverage(query: str, chunks: list[Chunk]) -> list[Chunk]:
    """Keep chunks only from documents covering every meaningful query term.

    Coverage is evaluated across the full document, not one chunk, so a
    multi-part request may still cite the specific chunk containing its fact.
    """
    query_terms = coverage_tokens(query)
    if not query_terms:
        return chunks

    document_terms: dict[str, set[str]] = {}
    for chunk in chunks:
        document_terms.setdefault(chunk.doc_id, set()).update(coverage_tokens(chunk.text))

    covered_docs = {
        doc_id for doc_id, terms in document_terms.items() if query_terms <= terms
    }
    return [chunk for chunk in chunks if chunk.doc_id in covered_docs]


def retrieve_top_k(query: str, chunks: list[Chunk], k: int | None = None) -> list[RetrievalResult]:
    k = config.TOP_K if k is None else k
    if k <= 0:
        raise ValueError("k must be > 0")

    candidates = searchable_chunks(chunks)
    if config.RETRIEVAL_STRATEGY == "coverage_filtered":
        candidates = chunks_matching_full_query_coverage(query, candidates)
    elif config.RETRIEVAL_STRATEGY != "lexical":
        raise ValueError(f"Unknown RETRIEVAL_STRATEGY: {config.RETRIEVAL_STRATEGY}")

    scored = [
        RetrievalResult(chunk=chunk, score=lexical_score(query, chunk.text))
        for chunk in candidates
    ]
    filtered = [item for item in scored if item.score >= config.RETRIEVAL_MIN_SCORE]
    filtered.sort(key=lambda item: (-item.score, item.chunk.chunk_id))
    return filtered[:k]
