from dataclasses import dataclass
import re

from . import config
from .corpus import Document


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    version: str
    status: str
    text: str


def split_text_with_overlap(text: str, chunk_size: int = 140, overlap: int = 30) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    chunks: list[str] = []
    start = 0
    step = chunk_size - overlap

    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(cleaned):
            break
        start += step

    return chunks


def split_text_by_sentences(text: str, chunk_size: int = 140) -> list[str]:
    """Pack complete sentences into chunks up to ``chunk_size`` characters.

    A sentence that is longer than the limit stays intact as a chunk so that
    factual statements are never cut in the middle merely to meet the limit.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    sentences = re.findall(r"[^.!?]+[.!?]+|[^.!?]+$", cleaned)
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        candidate = f"{current} {sentence}".strip()
        if current and len(candidate) > chunk_size:
            chunks.append(current)
            current = sentence
        else:
            current = candidate

        if len(current) > chunk_size:
            chunks.append(current)
            current = ""

    if current:
        chunks.append(current)
    return chunks


def split_text(text: str) -> list[str]:
    if config.CHUNK_STRATEGY == "chars":
        return split_text_with_overlap(text, chunk_size=config.CHUNK_SIZE, overlap=config.CHUNK_OVERLAP)
    if config.CHUNK_STRATEGY == "sentences":
        return split_text_by_sentences(text, chunk_size=config.CHUNK_SIZE)
    raise ValueError(f"Unknown CHUNK_STRATEGY: {config.CHUNK_STRATEGY}")


def build_chunks(documents: list[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in documents:
        for i, part in enumerate(split_text(doc.text)):
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.doc_id}-chunk-{i}",
                    doc_id=doc.doc_id,
                    title=doc.title,
                    version=doc.version,
                    status=doc.status,
                    text=part,
                )
            )
    return chunks
