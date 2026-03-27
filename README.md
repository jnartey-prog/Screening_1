# Resonance Risk Screening

Python package for physics-guided reduced-order screening of harmonic resonance susceptibility in 33/11 kV substations.

This repository is limited to the files needed to reproduce the released screening analysis and manuscript artifacts from the cleaned operational dataset.

## Reproducibility Contents

- `src/resonance_risk_screening/`: core preprocessing, proxy, clustering, scoring, and validation code
- `scripts/ingest_operational_workbook.py`: workbook-to-analysis ingest script
- `manuscript/generate_research_artifacts.py`: artifact generation script
- `data/substation_scada_33_11kv.csv`: cleaned analysis dataset
- `manuscript/artifacts/`: manuscript-facing figures, tables, and result files
- `manuscript/artifacts/research/data_provenance.yaml`: provenance summary
- `FINAL_RUN_MANIFEST.yaml`: frozen run manifest

## Quick Start

```bash
uv run python manuscript/generate_research_artifacts.py --data-path data/substation_scada_33_11kv.csv
```

## Workflow

1. Load and preprocess operational data.
2. Compute physics-guided proxies.
3. Reconstruct operating states.
4. Estimate resonance-risk score and class probabilities.
5. Generate manuscript tables and figures.
