# Skill: Generate Specs

**Description:** Generate specification documents A1-A6.
**Roles:** R2 (Architect), R3 (Domain Scientist)
**Inputs:** `proposal.normalized.json`, `BLUEPRINT-Universal-1_1.md`

## Steps

1.  **Analyze Proposal**
    - Identify Objectives, Data sources, and constraints.
    - Expand `Methodology & Analysis Plan.steps[]` into implementation-ready task seeds.
    - Extract all `manuscript_requirements.tables[]` and `manuscript_requirements.figures[]` as required deliverables.

2.  **Generate A1 (Project Definition)**
    - File: `specs/A1.md`
    - Content: Package name, versioning, constraints, success criteria.

3.  **Generate A2 (Features & API)**
    - File: `specs/A2.md`
    - Content: Public API signatures (Typed), Docstrings, Feature IDs.
    - **Requirement:** Must include a simple, user-friendly Python interface (short functions + sensible defaults).

4.  **Generate A3 (Architecture)**
    - File: `specs/A3.md`
    - Content: Directory structure (`src/` layout), Class hierarchy (UML/Text), Dependencies.

5.  **Generate A4 (Data & Tests)**
    - File: `specs/A4.md`
    - Content: Data schemas, Test plan (Unit/Integration/Acceptance), Traceability matrix.
    - Ensure every methodology step has at least one mapped test or validation task.

6.  **Generate A5 (Quality & CI)**
    - File: `specs/A5.md`
    - Content: Linting rules (ruff), Testing tools (pytest), CI workflow (GitHub Actions), and observability requirements.
    - Define persisted logging requirements (run logs + statistics logs), schema fields, and validation criteria.
    - Include coding standards: reuse library components before custom builds, and prohibit redundant/duplicate code paths.

7.  **Generate A6 (UX & Accessibility)**
    - File: `specs/A6.md`
    - Content: Non-coder personas, user-friendly Python interface design, defaults.

8.  **Review**
    - Verify that every Objective in Proposal maps to at least one Feature in A2.
    - Verify all required manuscript tables/figures are represented in specs and planned outputs.
    - Verify `tasks.seed.yaml` includes all methodology steps with owners and validation hooks.
