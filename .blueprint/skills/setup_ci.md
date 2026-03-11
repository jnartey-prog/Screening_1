# Skill: Setup CI

**Description:** Configure Continuous Integration workflows (GitHub Actions).
**Roles:** R5 (Tester), R2 (Architect)
**Inputs:** `specs/A5.md` (CI Config)

## Steps

1.  **Create Workflow**
    - Create `.github/workflows/ci.yml`.

2.  **Define Jobs**
    - **Environment:** Run `uv sync --all-extras`.
    - **Lint:** Run `ruff check .` and `ruff format --check .`.
    - **Type Check:** Run `mypy .`.
    - **Test:** Run `uv run pytest --cov`.
    - **Logging Compliance:** Run `uv run pytest -k logging -v`.
    - **Artifacts:** Run manuscript artifact generation and validation tests.
    - **Build:** Run `uv build`.

3.  **Matrix Strategy**
    - Test across Python versions (3.9, 3.10, 3.11, 3.12).
    - Test across OS (Ubuntu, Windows, macOS).

4.  **Artifacts**
    - Upload coverage reports.
    - Upload built wheels.
