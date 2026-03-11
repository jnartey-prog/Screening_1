# Skill: Phase -1 Expert Panel Normalization

**Description:** Standardize unstructured project documents into `proposal.normalized.json` using the Phase -1 three-expert panel workflow.
**Roles:** R1 (Orchestrator), R3 (Domain Scientist), R7 (RPM)
**Inputs:** Concept/Idea file, Manuscript Outline file, Literature Notes file, `BLUEPRINT-Universal-1_1.md`

## Steps

1.  **Ingest Source Documents**
    - Read all provided files (`.docx`, `.pdf`, `.md`, `.txt`).
    - Build a normalized text bundle with source tags: `concept`, `outline`, `literature`.

2.  **Create Independent Panel Drafts**
    - Generate `proposal_E1.json`, `proposal_E2.json`, `proposal_E3.json` independently.
    - Enforce Section 2.1 schema and avoid placeholders in critical fields.

3.  **Mandatory Mapping Rules**
    - Map concept content to: `Title`, `Scope`, `Objectives[]`, novelty, and key risks.
    - Map outline content to: `Methodology & Analysis Plan.steps[]` and all `manuscript_requirements.tables[]` + `figures[]`.
    - Map literature notes to: `literature_context.provided_notes` + `literature_context.key_references[]`.
    - Define `Observability & logging` profile (structured format, schemas, storage path, retention, redaction).

4.  **Algorithm Detail Expansion**
    - Convert each ordered outline methodology step into a concrete entry in `Methodology & Analysis Plan.steps[]`.
    - Create `tasks.seed.yaml` so each methodology step has at least one task seed with:
      - `task_id`
      - `title`
      - `assigned_to`
      - `validation_hook`

5.  **Merge and Resolve Conflicts**
    - Apply Phase -1 merge policy (consensus/majority/deliberation).
    - Record contested-field resolutions in `DECISIONS.md`.

6.  **DoR Validation**
    - Run Section 5.2 checks on merged proposal.
    - If failed: produce validation report and stop.
    - If passed: save canonical `proposal.normalized.json`.

## Success Criteria
- `proposal.normalized.json` is generated and DoR-ready.
- Every outline methodology step appears in `Methodology & Analysis Plan.steps[]`.
- Every required table/figure from outline appears in `manuscript_requirements`.
- `literature_context` is populated for downstream R7 BibTeX generation.
- `tasks.seed.yaml` exists with one or more seeds per methodology step.

## Autonomy Level
- Fully autonomous for extraction, mapping, and merge logic.
- Ask user only when source files are missing, unreadable, or contradictory on critical fields.
