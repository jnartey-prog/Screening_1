# Skill: Implement User-Friendly Python Interface

**Description:** Create a simple, high-level Python API for non-coders (Pythonic naming and defaults).
**Roles:** R4 (Implementer), R6 (Documenter)
**Inputs:** `specs/A2.md` (API), `specs/A6.md` (UX)

## Steps

1.  **Top-Level Functions**
    - In `src/<pkg>/__init__.py`, expose simple functions (e.g., `read()`, `analyze()`, `plot()`) that wrap the complex OO classes.
    - Ensure these functions have intuitive names and sensible defaults.

2.  **Rich Display**
    - Implement `__repr__` and `__str__` for all core classes to provide readable terminal output (e.g., summary tables).
    - Implement `_repr_html_` for Jupyter Notebook integration.

3.  **Method Chaining**
    - Ensure core classes support method chaining (return `self` where appropriate) to allow pipelines like `data.load().clean().plot()`.

4.  **Interactive Plots**
    - Implement `plot()` methods that launch interactive visualizations (using matplotlib/plotly).

5.  **Templates**
    - Create `examples/analysis_template.py` for copy-paste workflows.
