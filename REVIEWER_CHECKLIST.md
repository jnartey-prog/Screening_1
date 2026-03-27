# Reviewer Traceability Checklist

## Data Lineage

- [x] Raw source workbook identified: `data/data_table.xlsx`
- [x] Deterministic ingest script provided: `scripts/ingest_operational_workbook.py`
- [x] Analysis dataset specified: `data/substation_scada_33_11kv.csv`
- [x] Provenance summary included: `manuscript/artifacts/research/data_provenance.yaml`
- [x] Frozen run manifest included: `FINAL_RUN_MANIFEST.yaml`
- [x] Artifact hashes recorded: `manuscript/artifacts/research/ARTIFACT_HASHES.sha256`

## Methods Transparency

- [x] Date parsing and timestamp harmonization rules documented
- [x] Column mapping from workbook to analysis channels documented
- [x] Missing-data fallback rules documented
- [x] Inclusion/exclusion criteria documented
- [x] Coverage limitations noted

## Required Tables (Outline Alignment)

- [x] Table 1: symbols, variables, units, notation
- [x] Table 2: dataset channels and data-quality flags
- [x] Table 3: proxy definitions and physical interpretation
- [x] Table 4: clustering settings and selection criteria
- [x] Table 5: ordinal risk labels and thresholds
- [x] Table 6: benchmark performance comparison
- [x] Table 7: sensitivity/robustness summary

## Required Figures (Outline Alignment)

- [x] Figure 1: conceptual framework
- [x] Figure 2: workflow (preprocess -> proxies -> clustering -> risk model)
- [x] Figure 3: time-series behavior (load/voltage/incomer/feeder)
- [x] Figure 4: proxy distribution and correlation structure
- [x] Figure 5: clustering results and medoid states
- [x] Figure 6: ordinal model outputs / key proxy effect plots
- [x] Figure 7: benchmark and uncertainty/sensitivity visualization

## Artifact Quality

- [x] Publication-ready figure exports: PNG (600 dpi), PDF, SVG
- [x] Table exports: CSV and LaTeX
- [x] Canonical folders synchronized:
  - `manuscript/artifacts/research` (master publication package)
  - `manuscript/artifacts` (manuscript insertion-compatible names)

## Remaining External Items

- [ ] External preregistration upload confirmation
- [ ] Remote CI evidence bundle attachment for clean-branch matrix run
