# Data Provenance and Reproducibility

This project now includes an explicit ingest path from the original field workbook to the analysis dataset used by the screening pipeline.

## Source File

- `MALLAM BSP HOURLY READINGS, 2024.xlsx` (raw field workbook)

## Ingest Script

- `scripts/ingest_mallam_field_data.py`

The script parses monthly workbook sheets, extracts hourly operational channels, constructs timestamps, and writes an analysis-ready CSV with pipeline-compatible columns:

- `timestamp`
- `v_bus`
- `i_inc`
- `p_total`
- `i_f_1`
- `i_f_2`
- `i_f_3`

It also writes a provenance report:

- `manuscript/artifacts/research/data_provenance.yaml`

## Reproduction Commands

Run from repository root:

```powershell
.\.venv\Scripts\python.exe scripts\ingest_mallam_field_data.py `
  --input "MALLAM BSP HOURLY READINGS, 2024.xlsx" `
  --output data\substation_scada_33_11kv_field.csv `
  --provenance manuscript\artifacts\research\data_provenance.yaml
```

Generate manuscript research artifacts from field-derived data:

```powershell
.\.venv\Scripts\python.exe manuscript\generate_research_artifacts.py `
  --data-path data\substation_scada_33_11kv_field.csv
```

Run core pipeline outputs from field-derived data:

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -c "from pathlib import Path; from resonance_risk_screening.pipeline import ResonancePipeline; ResonancePipeline().run(Path('data/substation_scada_33_11kv_field.csv'), Path('manuscript/artifacts'))"
```

## Notes

- `data/` is git-ignored in this repository, so generated CSV datasets are not versioned by default.
- The provenance YAML is the authoritative run summary for source file, parsed rows, time span, sheets used, and channel statistics.
