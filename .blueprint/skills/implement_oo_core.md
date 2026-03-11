# Skill: Implement OO Core

**Description:** Implement the core Object-Oriented class hierarchy.
**Roles:** R4 (Implementer)
**Inputs:** `specs/A2.md` (API), `specs/A3.md` (Architecture), `specs/A6.md` (Design)

## Steps

1.  **Abstract Base Classes**
    - Define ABCs (e.g., `BaseModel`, `BaseDataset`) in `src/<pkg>/core/`.
    - Define abstract methods (`fit`, `predict`, `load`).

2.  **Concrete Classes**
    - Implement concrete classes inheriting from ABCs.
    - Place in appropriate modules (`src/<pkg>/models/`, etc.).
    - Reuse standard-library or third-party components where they already satisfy requirements; avoid unnecessary custom rewrites.

3.  **Type Hints & Docs**
    - Add Python type hints to ALL methods.
    - Add Google-style docstrings to ALL methods/classes.

4.  **Encapsulation**
    - Use properties (`@property`) for data access.
    - Use `_private` attributes for internal state.

5.  **Design Patterns**
    - Apply patterns from A3 (Factory, Strategy, Observer).

6.  **Observability Hooks**
    - Add centralized logger usage in core workflows (`fit`, `predict`, `run`, data load/save).
    - Emit structured run events and statistics summaries using the schemas defined in A5.
    - Ensure logs can be persisted to configured storage paths.

7.  **Redundancy Check**
    - Remove duplicate or dead code paths created during implementation.
    - Consolidate repeated logic into shared utilities/modules.
