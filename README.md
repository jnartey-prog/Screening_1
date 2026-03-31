# Resonance Risk Screening

Python package for physics-guided reduced-order screening of harmonic resonance susceptibility in 33/11 kV substations.

This repository is limited to the code and run-manifest files required to document the released screening workflow.

## Reproducibility Contents

- `src/resonance_risk_screening/`: core preprocessing, proxy, clustering, scoring, and validation code
- `scripts/ingest_operational_workbook.py`: workbook-to-analysis ingest script
- `manuscript/generate_research_artifacts.py`: artifact generation script
- `FINAL_RUN_MANIFEST.yaml`: frozen run manifest

## Quick Start

```bash
uv run python manuscript/generate_research_artifacts.py
```

## Workflow

1. Load and preprocess operational data.
2. Compute physics-guided proxies.
3. Reconstruct operating states.
4. Estimate resonance-risk score and class probabilities.
5. Generate manuscript tables and figures.
