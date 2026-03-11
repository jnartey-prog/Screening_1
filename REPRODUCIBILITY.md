# Reproducibility Guide

## Environment

1. Install Python 3.10-3.12.
2. Install dependencies:

```bash
uv sync --extra dev
```

## Run Pipeline

```bash
uv run resonance-pipeline --input path/to/data.csv --output-dir manuscript/artifacts
```

Outputs include predictions, validation metrics, benchmarks, manuscript tables, and manuscript figures.

## Run Tests

```bash
uv run pytest -q
```

## Full Reproduction Replay

```bash
uv run python scripts/reproduce_all.py
```

This replay runs manuscript artifact generation and verifies required output files and manifest paths.

## Determinism and Logging

- Clustering/model steps use fixed seeds where applicable.
- Runtime logs are written to `logs/run.log` and `logs/run.jsonl`.
- Statistics and benchmark outputs are persisted in output artifacts.
