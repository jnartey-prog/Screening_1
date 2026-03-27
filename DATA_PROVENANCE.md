# Data Provenance and Reproducibility

This project now includes an explicit ingest path from the source operational workbook to the analysis dataset used by the screening pipeline.

## Source File

- `data/data_table.xlsx` (source operational workbook)

## Ingest Script

- `scripts/ingest_operational_workbook.py`

The script parses the workbook sheets, extracts hourly operational channels, constructs timestamps, and writes an analysis-ready CSV with pipeline-compatible columns:

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
.\.venv\Scripts\python.exe scripts\ingest_operational_workbook.py `
  --input data\data_table.xlsx `
  --output data\substation_scada_33_11kv.csv `
  --provenance manuscript\artifacts\research\data_provenance.yaml
```

Generate manuscript research artifacts from the cleaned analysis dataset:

```powershell
.\.venv\Scripts\python.exe manuscript\generate_research_artifacts.py `
  --data-path data\substation_scada_33_11kv.csv
```

Run core pipeline outputs from the cleaned analysis dataset:

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -c "from pathlib import Path; from resonance_risk_screening.pipeline import ResonancePipeline; ResonancePipeline().run(Path('data/substation_scada_33_11kv.csv'), Path('manuscript/artifacts'))"
```

## Notes

- The cleaned analysis CSV is the dataset used by the released manuscript artifacts.
- The provenance YAML is the authoritative run summary for source file, parsed rows, time span, sheets used, and channel statistics.
