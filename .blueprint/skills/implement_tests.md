# Skill: Implement Tests

**Description:** Implement a comprehensive test suite using pytest.
**Roles:** R5 (Tester), R4 (Implementer)
**Inputs:** `specs/A4.md` (Test Plan), `specs/A5.md` (Quality)

## Steps

1.  **Fixtures**
    - Create `tests/conftest.py`.
    - Implement fixtures for synthetic data generation and common objects.

2.  **Unit Tests**
    - Create `tests/test_<module>.py` for each source module.
    - Test every public method in isolation.
    - Use `@pytest.mark.parametrize` for edge cases.

3.  **Integration Tests**
    - Test interactions between modules (e.g., Pipeline -> Model -> Result).
    - Verify user-friendly Python interface workflows.
    - Verify persisted logging behavior (run log and statistics log files + required fields).

4.  **Acceptance Tests**
    - Implement tests that directly verify the Objectives from the Proposal.
    - Mark these with `@pytest.mark.acceptance`.

5.  **Configuration**
    - Update `pyproject.toml` with coverage settings (`[tool.coverage]`).
    - Ensure `pytest` runs correctly.
    - Add logging test markers/selectors for CI (for example `-k logging`).
