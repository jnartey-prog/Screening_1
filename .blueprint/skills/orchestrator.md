# Skill: Orchestrator

**Description:** Autonomously build a complete Python package following BLUEPRINT-Universal-1.1 from proposal to release.
**Roles:** R1 (Orchestrator)
**Inputs:** `proposal.normalized.json` (optional), `BLUEPRINT-Universal-1_1.md`

## Workflow

1.  **Initialize**
    - Load `.blueprint/config.yaml` and `.blueprint/state.json`.
    - Check if `proposal.normalized.json` exists.
    - IF MISSING: Trigger `skills/idea_to_proposal`.
    - IF PRESENT: Proceed to Step 2.

2.  **Validate Proposal**
    - Execute `skills/validate_proposal`.
    - IF FAILED: Stop and report issues.
    - IF PASSED: Update state to `PHASE_1_SPECS`.

3.  **Generate Specifications (A1-A6)**
    - Execute `skills/generate_specs`.
    - **User Review:** Ask user to review `specs/`.
    - Update state to `PHASE_2_SETUP`.

4.  **Package Setup**
    - Execute `skills/setup_package`.
    - Update state to `PHASE_3_IMPLEMENT`.

5.  **Core Implementation**
    - Execute `skills/implement_oo_core`.
    - Update state to `PHASE_3_IMPLEMENT_INTERFACE`.

6.  **User-Friendly Python Interface Implementation**
    - Execute `skills/implement_python_interface`.
    - Update state to `PHASE_4_TEST`.

7.  **Test Implementation**
    - Execute `skills/implement_tests`.
    - Update state to `PHASE_5_ARTIFACTS`.

8.  **Publication Artifact Plotting**
    - Execute `skills/plot_publication_artifacts`.
    - Update state to `PHASE_5_DOCS`.

9.  **Documentation Setup**
    - Execute `skills/setup_docs`.
    - Update state to `PHASE_6_CI`.

10. **CI/CD Setup**
    - Execute `skills/setup_ci`.
    - Update state to `PHASE_7_VERIFY`.

11. **Final Validation**
    - Execute `skills/final_validation`.
    - **User Review:** Present `VALIDATION_REPORT.md`.

12. **Completion**
    - Update state to `COMPLETED`.
    - Generate final success report.
