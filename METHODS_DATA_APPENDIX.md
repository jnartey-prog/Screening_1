# Methods Data Appendix

## Scope

This appendix documents the exact data transformation path used for the current manuscript artifacts:

- Raw source: `data/data_table.xlsx`
- Ingest script: `scripts/ingest_operational_workbook.py`
- Analysis dataset: `data/substation_scada_33_11kv.csv`
- Provenance summary: `manuscript/artifacts/research/data_provenance.yaml`

The source workbook is treated in this repository as a restricted operational record. The retained analysis window in the current frozen run is:

- Start timestamp: `2024-01-01 00:00:00`
- End timestamp: `2024-04-01 07:00:00`
- Valid retained rows: `2082`
- Contributing sheets: `Sheet2`

This replaces any earlier vague phrasing such as "approximately one year." The current manuscript artifacts are based on the exact window above.

## Source Channel Manifest

The workbook header rows expose the following source channels and units:

- date and hour fields
- incomer current channels
- aggregate incomer current labeled `TOTAL (KA)` in the workbook
- busbar voltage channel(s) in `kV`
- incomer power channels in `MW`
- aggregate real power in `MW`
- feeder current channels

Only the analysis channels required by the screening pipeline are retained in the final CSV:

- `timestamp`
- `v_bus`
- `i_inc`
- `p_total`
- `i_f_1`
- `i_f_2`
- `i_f_3`

## Workbook Parsing Rules

- The workbook is parsed from OOXML sheet XML (`xl/worksheets/sheet*.xml`).
- Workbook tabs are discovered from `workbook.xml` relationship mapping.
- Shared strings are resolved from `sharedStrings.xml`.
- If explicit date text is absent, Excel serial date is used when present.
- Hour index is accepted only for `1..24`.
- Timestamp is set as `date + (hour - 1)`.

## Channel Mapping (Raw -> Analysis)

- `timestamp` <- derived from date block + hourly index (`B`)
- `i_inc` <- aggregate current field; fallback = sum of incomer-current channels when needed
- `v_bus` <- mean of available busbar-voltage channels
- `p_total` <- aggregate total-MW field; fallback = sum of incomer MW channels
- `i_f_1`, `i_f_2`, `i_f_3` <- first three available feeder numeric channels

The feeder-current reduction to `i_f_1:i_f_3` is a modelling choice made for a complete and consistent reduced-order dataset. The original workbook contains additional feeder channels beyond the three retained analysis features.

## Row Inclusion/Exclusion Logic

- Keep row only if:
  - valid date context exists
  - valid hour in `1..24`
  - `i_inc`, `v_bus`, `p_total`, `i_f_1..i_f_3` are all available after fallback rules
- After parsing all sheets:
  - sort by `timestamp`
  - drop duplicate timestamps (keep first)

## Quality Controls Reported

`data_provenance.yaml` records:

- source file path
- output file path
- rows parsed
- start/end timestamp
- sheets contributing retained rows
- per-channel min/max/mean/missing-rate
- screened-outlier counts

## Important Data-Coverage Note

The workbook includes months/sheets with sparse or placeholder-like blocks. The ingest keeps only rows meeting the strict completeness criteria above; therefore the final analysis window reflects valid retained field rows rather than all nominal workbook rows.

## Reproducibility Boundary

This repository supports computational reproducibility from the raw workbook to the final analysis dataset and derived manuscript artifacts. It does not, by itself, provide a full utility engineering dossier. Metadata such as SCADA vendor, relay/instrument model numbers, calibration certificates, transformer nameplate ratings, capacitor-bank switching records, feeder impedance parameters, and utility data-sharing identifiers are not present in the workbook and are therefore not asserted in the released computational package.
