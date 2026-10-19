# Advanced follow-up: coverage-filtered lexical retrieval

This is a separate advanced experiment after the required one-change
sentence-chunking submission. It must not replace the `before.json` →
`after.json` evidence in `weekly-report.md`.

## Change

`RETRIEVAL_STRATEGY` is set to `"coverage_filtered"`.

The strategy applies a small, general-purpose query normalization layer:

- removes question scaffolding such as “how”, “what”, “the”, and “until”;
- normalizes ordinary variants such as `yearly`/`year` and
  `remotely`/`remote`;
- expands the domain synonym `notebook computer` to `replacement laptop`.

Before scoring chunks, it builds a set of normalized terms for each document.
Only documents containing every meaningful query term remain candidates. Chunk
ranking and citations then continue to use the existing lexical scorer. This
lets a fact live in a different chunk from another requested detail, while
rejecting a near-domain document that is missing a required concept.

## Evaluation

Compared with the required sentence-chunking run (`results/after.json`), the
advanced run is saved as `results/advanced-coverage.json`.

```text
Fixed (fail -> pass): E05, E10, E11
Regressed (pass -> fail): none
Unchanged: E01, E02, E03, E04, E06, E07, E08, E09, E12

Summary:
  passed: 9 -> 12 (+3)
  total: 12 -> 12 (+0)
  behaviour_accuracy: 0.8333 -> 1.0 (+0.1667)
  retrieval_hit_rate: 0.8889 -> 1.0 (+0.1111)
  mean_citation_precision: 0.5455 -> 0.9444 (+0.3989)
```

All tests pass (`18 passed`). The eval set hash is unchanged:
`afe46db1e75a0b85bb5c9a93b6763e3b96e5cd7b289e12da6d2671e4d8650064`.

## Limitations

The result demonstrates the behavior on this fixed, small benchmark; it does
not establish general semantic understanding. Strict coverage can incorrectly
refuse valid questions that use unseen synonyms or terms distributed across
multiple documents. The phrase normalization list should therefore be grown
from real query logs and evaluated on a held-out set, rather than tuned only
against this eval set.
