# Skill: Validate Proposal

**Description:** Validate `proposal.normalized.json` against the Definition of Ready (DoR).
**Roles:** R1 (Orchestrator), R3 (Domain Scientist)
**Inputs:** `proposal.normalized.json`

## Steps

1.  **Read Artifacts**
    - Read `proposal.normalized.json`.
    - Read `BLUEPRINT-Universal-1_1.md` (Section 5.2).

2.  **Verify Schema**
    - Check if all required fields are present (Title, Scope, Objectives, Data, etc.).
    - Check for placeholders (TBD, ???).

3.  **Verify Data**
    - Check if data URLs are valid/reachable.
    - Check if license information is present.

4.  **Verify Novelty**
    - If `Novelty flag` is true, check for `Preregistration URL`.

5.  **Verify Observability**
    - Check `Observability & logging` is present with required schema/storage fields.

6.  **Generate Report**
    - Create `validation-report.md`.
    - List all checks as [PASS] or [FAIL].

7.  **Decision**
    - If any [FAIL], stop workflow.
    - If all [PASS], mark proposal as READY.
