# Skill: Final Validation

**Description:** Perform a final quality audit before release.
**Roles:** R1 (Orchestrator), R5 (Tester), R7 (RPM)
**Inputs:** All artifacts

## Steps

1.  **Audit Checklist**
    - [ ] Proposal DoR Passed?
    - [ ] Specs A1-A6 Complete & Consistent?
    - [ ] Package Environment Resolves (`uv sync`)?
    - [ ] Tests Pass (100%)?
    - [ ] Coverage > Threshold?
    - [ ] Persisted Logging Implemented (run + statistics logs)?
    - [ ] Logging Schema Compliance Tests Pass?
    - [ ] Library-First Coding Standard Followed (no unnecessary custom components)?
    - [ ] No Redundant/Duplicate Production Code Paths?
    - [ ] Plotting Mechanism Implemented (manifest + generators + pipeline entrypoint)?
    - [ ] Artifact Generation Smoke Test Passes (when fixture data is available)?
    - [ ] Publication Plot Quality Rules Implemented (format/DPI/style)?
    - [ ] Linting Clean?
    - [ ] Type Checks Clean?
    - [ ] Docs Build Clean?
    - [ ] Traceability Matrix Complete?
    - [ ] Reproducibility Guide Tested?

2.  **Generate Report**
    - Create `VALIDATION_REPORT.md` summarizing the audit.
    - List any remaining issues.
    - Clearly separate mechanism checks from full analysis/reproduction artifact runs.

3.  **Release Decision**
    - IF score < 100%: FAIL.
    - IF score = 100%: PASS -> Ready for Release.
