# Skill: Setup Package

**Description:** Create the Python package directory structure and configuration.
**Roles:** R2 (Architect), R4 (Implementer)
**Inputs:** `specs/A1.md`, `specs/A3.md`

## Steps

1.  **Create Directories**
    - Create `src/<package_name>/`, `tests/`, `docs/`, `examples/`.
    - Create submodules defined in A3 (e.g., `core/`, `models/`, `utils/`).

2.  **Create Metadata**
    - Create `pyproject.toml` (PEP 621).
    - Include: dependencies, dependency groups, build-system, tool configs (ruff, pytest), and `tool.uv` configuration.

3.  **Create Initialization**
    - Create `src/<package_name>/__init__.py`.
    - Expose public API (from A2).
    - Define `__version__`.

4.  **Create Observability Foundation**
    - Create package logging configuration module (e.g. `src/<package_name>/logging_config.py`).
    - Define default persisted log paths and structured log format.
    - Add runtime log directories to `.gitignore` (for example `logs/`).

5.  **Create Support Files**
    - Create `README.md` (Skeleton).
    - Create `.gitignore` (Python standard).
    - Create `LICENSE` file.

6.  **Verify**
    - Run `uv sync` to ensure the project environment resolves and installs correctly.
