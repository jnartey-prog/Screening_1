# Skill: Plot Publication-Grade Artifacts

**Description:** Implement reproducible, publication-grade figure generation aligned to `manuscript_requirements` and methodology outputs.
**Roles:** R6 (Documenter), R4 (Implementer), R5 (Tester)
**Inputs:** `proposal.normalized.json`, `specs/A2.md`, `specs/A3.md`, `specs/A4.md`, `tasks.seed.yaml` (if present)

## Steps

1.  **Build Artifact Manifest**
    - Read `Methodology & Analysis Plan.manuscript_requirements`.
    - Create `manuscript/artifact_manifest.yaml` mapping each required table/figure to:
      - source data/query
      - generator function
      - output path(s)
      - validation check

2.  **Define Plot Style System**
    - Create a reusable plotting style module/config (fonts, line widths, palettes, markers, legend conventions).
    - Enforce publication defaults:
      - vector output (`.pdf`/`.svg`) plus raster (`.png`)
      - minimum 300 DPI (600 DPI for print-critical plots)
      - colorblind-safe palette and grayscale-safe contrast
      - deterministic seeds for stochastic visuals

3.  **Implement Figure/Table Generators**
    - Implement generators under package manuscript/artifact modules.
    - Ensure each required figure/table has a dedicated callable generator.
    - Keep plotting logic separate from business logic and data loading.

4.  **Pipeline Integration**
    - Add/extend a single entrypoint (for example `generate_artifacts`) that can regenerate manuscript outputs after analysis.
    - Ensure outputs are written to `manuscript/artifacts/` using stable filenames.
    - Do not require full-data artifact generation during package setup validation.

5.  **Quality Validation**
    - Add tests that verify:
      - every required table/figure has a manifest entry and callable generator
      - output formats and naming rules are enforced by generator configuration
      - smoke-generation works on fixture data (when available)
      - basic visual constraints (size, DPI where applicable) are checked in generated outputs

6.  **Documentation**
    - Document the artifact pipeline, style rules, and regeneration command in `REPRODUCIBILITY.md` and user docs.

## Success Criteria
- Every required figure/table in `manuscript_requirements` is covered by implemented generators.
- Artifacts are reproducible with one command and deterministic inputs.
- Publication-grade defaults (format, DPI, readability) are enforced.
- Tests validate mechanism completeness; output-quality checks run in smoke/integration mode when data exists.

## Autonomy Level
- Fully autonomous for design and implementation decisions that do not alter scientific conclusions.
- Ask user only when manuscript requirements are ambiguous or contradictory.
