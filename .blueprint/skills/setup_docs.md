# Skill: Setup Documentation

**Description:** Set up Sphinx documentation and generate API docs.
**Roles:** R6 (Documenter)
**Inputs:** `specs/A1.md`, `specs/A2.md`

## Steps

1.  **Initialize Sphinx**
    - Run `sphinx-quickstart` in `docs/` (or create manually).
    - Configure `conf.py` to use `sphinx_rtd_theme` (or similar).
    - Enable `sphinx.ext.autodoc`, `sphinx.ext.napoleon` (for Google-style docstrings), `sphinx.ext.viewcode`.

2.  **Create Index**
    - specific `index.rst` with sections:
        - Installation
        - Quick Start (User-friendly Python guide)
        - API Reference
        - Tutorials

3.  **API Reference**
    - Use `.. automodule::` directives to pull docstrings from `src/`.

4.  **Build**
    - Run `make html` in `docs/`.
    - Verify no warnings/errors.
