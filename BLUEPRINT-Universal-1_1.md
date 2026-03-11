# BLUEPRINT-Universal-1.1 (Python Edition)

**Subtitle:** Research-Grade Python Package DNA with Mandatory Interactive Pipeline

Version: 1.1-py
Status: Draft / Internal Standard
Owner: (fill in)
Last updated: (fill in)
Language: Python 3.9+

---

## 0. Purpose & Scope

This blueprint defines a **standardized process ("DNA")** for building research-grade **Python packages** from a structured proposal, following Python packaging standards (PEPs) and best practices.

It is designed so that both **humans and AI agents** can:

1. Take a **proposal** (Title, Scope, Objectives, Data, Novelty, Risks),
2. **Establish a configured agent team** with defined roles and tools,
3. Produce a **fully specified Python package** (A1–A5 specs, tasks, architecture),
4. Implement and test the code following Python conventions,
5. Deliver a **installable, PyPI-ready package with an interactive pipeline workflow**.

The blueprint is **domain-agnostic** within Python ecosystems. It can be used for:

- New algorithms (e.g. N-PLS, federated chemometrics, neutrosophic AQbD),
- Analytical pipelines (e.g. exposure assessment, dose estimation),
- Tools & utilities (e.g. calibration transfer libraries),
- Scientific computing packages,
- Data processing frameworks.

Assumptions:

- The work can be described with a finite set of **Objectives**.
- The work can be implemented as a **Python package/library** with **tests**.
- The package must provide at least one **interactive pipeline entrypoint**.
- The package follows **Python Enhancement Proposals (PEPs)** for packaging (PEP 517, 518, 621).
- The package supports **Python 3.9+** (or specify minimum version in proposal).
- The package uses **uv** for environment and dependency management.
- The package is installable via standard wheel/sdist artifacts and distributable via PyPI or private repositories.

Design Philosophy:

- **Object-Oriented Architecture**: Python is an object-oriented language, and packages SHOULD leverage OO principles:
  - Encapsulation: Data and behavior bundled in classes
  - Inheritance: Code reuse through class hierarchies
  - Polymorphism: Flexible interfaces via abstract base classes
  - Composition: Building complex functionality from simple components

- **Accessibility for Non-Coders**: The package MUST be designed so non-programmers can accomplish common tasks:
  - **No-code interfaces**: GUI, web apps, or CLI wizards that require zero coding
  - **Minimal-code interfaces**: Simple, copy-paste examples for basic tasks
  - **Progressive complexity**: Easy entry point, with advanced features available for experienced users
  - **Clear error messages**: Human-readable errors with suggested solutions
  - **Sensible defaults**: Common use cases work out-of-the-box without configuration

---

## 1. AI Agent Operating Instructions

This section explains how AI agents MUST use this blueprint. It acts as a **mini system prompt** for any automated tooling that follows BLUEPRINT-Universal-1.1.

### 1.1 Priority of rules

1. This blueprint is **normative**:
   - **MUST** = hard requirement; do not skip.
   - **SHOULD** = strong recommendation; only skip with a clear written reason.
   - **MAY** = optional.

2. If instructions from outside this file conflict with this blueprint:
   - The Orchestrator (R1) MUST either:
     - (a) reject the conflicting instructions, or  
     - (b) record an explicit exception in `DECISIONS.md` (who, why, and what changed).

### 1.2 Global invariants (never break these)

AI agents MUST obey these invariants at all times:

1. **No work before readiness**  
   - Do NOT write production code until `proposal.normalized.json` passes the **Definition of Ready (DoR)** in Section 5.
   - If DoR fails, STOP and return a validation report; do not silently "fix" the proposal.

2. **No agents before establishment**  
   - Do NOT begin spec generation until Phase 1A has produced a valid `agents.yaml` with role assignments and tool manifests.
   - Agents without explicit tool authorization MUST NOT invoke those tools.

3. **No hidden logic**  
   - All significant design/implementation decisions MUST be written into `DECISIONS.md` with:
     - Role (R1–R7),
     - Date,
     - Decision,
     - Alternatives considered (if any),
     - Justification.

4. **Traceability is mandatory**  
   - Every Objective in the proposal MUST map to:
     - At least one feature in A2,
     - At least one test in A4,
     - At least one row in `TRACEABILITY.csv`.

5. **Interactive pipeline is not optional**  
   - You MUST implement at least one interactive pipeline workflow (Section 10).
   - It MUST be:
     - Documented in A2/A3,
     - Tested via at least one end-to-end test in A4,
     - Demonstrated in `examples/`.

6. **No placeholders in final state**  
   - In the final research-grade state, there MUST be:
     - No `TBD`, `TODO`, `???`, or `REPLACE-ME` strings in any spec (A1–A5),
     - No unimplemented stubs for public API functions.

### 1.3 Role-specific behaviours for AI agents

AI agents SHOULD adopt one or more of the roles R1–R7 when performing tasks. Each role is formally instantiated during **Phase 1A (ESTABLISH_AGENTS)** with an explicit tool manifest.

- **R1 – Orchestrator**
  - Always start with PHASE 0 (READ_PROPOSAL).
  - Leads Phase 1A to establish the agent team.
  - Enforce DoR (Section 5).
  - Decide when the project can move from one phase to the next (Section 8).
  - Record high-level decisions in `DECISIONS.md`.

- **R2 – Architect**
  - Owns the content and consistency of A1–A3.
  - MUST ensure every feature in A2 has:
    - A clear signature,
    - A place in the architecture (A3),
    - A link to at least one Objective.

- **R3 – Domain Scientist**
  - Ensures Objectives, Scope, and tests make scientific sense.
  - MUST verify that:
    - Proposed metrics are appropriate,
    - Datasets and simulations align with the domain.

- **R4 – Implementer**
  - Reads A2/A3 and `tasks.yaml` to implement code.
  - MUST:
    - Write code that matches A2 signatures and behaviour,
    - Write/extend tests indicated in `expected_tests`,
    - Never bypass A4's test plan.

- **R5 – Tester**
  - Runs tests and validates acceptance criteria from A4.
  - MUST:
    - Fail tasks when coverage/criteria are not met,
    - Escalate design issues back to R2/R3 via `DECISIONS.md`.

- **R6 – Documenter**
  - Owns user-facing docs and examples.
  - MUST ensure:
    - At least one working example of the interactive pipeline,
    - Docs match the actual API and behaviour.

- **R7 – RPM (Research Product Manager)**
  - Owns `TRACEABILITY.csv`, `LITERATURE.bib`, `REPRODUCIBILITY.md`, and preregistration.
  - MUST:
    - Keep traceability in sync with specs and code,
    - Confirm reproducibility instructions are correct.

Agents SHOULD annotate their actions with the role they are acting as (e.g. in commit messages or decision logs).

### 1.4 Phase-by-phase rules for agents (summary)

AI Orchestrator (R1) MUST enforce this order (see Section 8 for details):

1. **PHASE 0 – READ_PROPOSAL**
   - Validate `proposal.normalized.json` against DoR (Section 5).
   - Output: either an error report or "Proposal Ready".

2. **PHASE 1A – ESTABLISH_AGENTS**
   - Instantiate the agent team based on proposal complexity.
   - Assign roles, tools, and boundaries to each agent.
   - Output: `agents.yaml` with role configurations and tool manifests.

3. **PHASE 1B – GENERATE_SPECS**
   - R2/R3 generate A1–A5 from the proposal using their assigned tools.
   - Output: complete specs with no TBDs in core sections.

4. **PHASE 2 – BUILD_TASK_GRAPH**
   - Build `tasks.yaml` from A2/A3.
   - Output: acyclic task graph with clear `expected_tests`.

5. **PHASE 3 – IMPLEMENT**
   - R4 implements; R5 tests; R1 coordinates.
   - Output: working code + tests for all non-pipeline features.

6. **PHASE 4 – INTEGRATE_PIPELINE**
   - Implement interactive pipeline feature(s) and tests.
   - Output: pipeline CLI/notebook/web/TUI that passes end-to-end tests.

7. **PHASE 5 – GOVERN & DOCUMENT**
   - Fill `TRACEABILITY.csv`, `DECISIONS.md`, `LITERATURE.bib`, `REPRODUCIBILITY.md`.

8. **PHASE 6 – VERIFY & RELEASE**
   - Run full CI; verify Objective acceptance.
   - Tag release and record in `DECISIONS.md`.

Agents MUST NOT jump directly to PHASE 2 or later without completing earlier phases. Phase 1A is a prerequisite for Phase 1B.

### 1.5 Error handling & escalation

If an AI agent encounters:

- **Missing or contradictory specs** → escalate to R1/R2:
  - Add an entry in `DECISIONS.md` describing the issue.
  - Propose one or more resolutions.

- **Test failures that suggest spec errors** → R5 MUST:
  - Log the mismatch,
  - Request spec update instead of silently changing behaviour.

- **Tool invocation outside manifest** → R1 MUST:
  - Reject the action,
  - Log the violation in `DECISIONS.md`.

No silent corrections of the blueprint itself are allowed; changes to this blueprint MUST be recorded as a separate decision and version bump.

---

## 2. Inputs & Outputs

### 2.1 Required input: `proposal.normalized.json`

All work begins from a single machine-readable proposal file:

- File: `proposal.normalized.json`
- Format: JSON
- Required top-level fields:

  - `Title` – human-readable project title.  
  - `Scope` – clear description of what is in and out of scope.  
  - `Objectives[]` – list of objects with:
    - `statement` – short, testable objective,
    - `owner` – role ID (e.g. `"R3"`),
    - `acceptance` – ID of corresponding acceptance test,
    - `provenance.doi` – DOI or URL to primary reference (if applicable).  

  - `Data to be used[]` – each with:
    - `name`,
    - `url`,
    - `license`,
    - `pii_classification`,
    - `justification`.  

  - `Methodology & Analysis Plan` – object with:
    - `steps[]` – Ordered list of methodological steps (e.g. "1. Preprocessing", "2. Feature Selection"),
    - `mathematical_basis` – Reference to specific equations or algorithms,
    - `manuscript_requirements` – object with:
      - `tables[]` – List of required tables (e.g. "Table 1: Demographics", "Table 2: ANOVA results"),
      - `figures[]` – List of required figures (e.g. "Fig 1: Flowchart", "Fig 2: Response Surface").

  - `Novelty flag` – boolean (`true` if novel research).  
  - `Preregistration URL` – required if `Novelty flag` is `true`.  
  - `literature_context` – object with:
    - `provided_notes` – Raw text or summary of key literature provided by the user (supports rich context),
    - `key_references[]` – List of critical papers with `doi`, `citation`, and `relevance` (e.g. "Basis for Eq 2").

  - `Risks & mitigations[]` – each with:
    - `risk`,
    - `owner`,
    - `verification_method`.

  - `Python package specifics` – object with:
    - `pypi_name` – Package name as it will appear on PyPI (lowercase, hyphens allowed),
    - `import_name` – Python import name (lowercase, underscores, valid identifier),
    - `min_python_version` – Minimum Python version (e.g. `"3.9"`),
    - `max_python_version` – Maximum tested Python version (e.g. `"3.12"`, or `null`),
    - `requires_python` – PEP 440 version specifier (e.g. `">=3.9,<4.0"`),
    - `dependencies[]` – List of core dependencies with version constraints (e.g. `["numpy>=1.20", "pandas>=1.3"]`),
    - `optional_dependencies{}` – Object mapping extra names to dependency lists (e.g. `{"dev": ["pytest>=7.0", "ruff>=0.1"], "docs": ["sphinx>=5.0"]}`),
    - `console_scripts[]` – List of CLI entry points (e.g. `["mytool-cli=mytool.cli:main"]`),
    - `python_typing` – Boolean indicating if package includes type hints (PEP 484),
    - `package_layout` – Either `"src"` (recommended) or `"flat"`,
    - `build_backend` – Build system backend (e.g. `"setuptools"`, `"hatchling"`, `"flit_core"`, `"pdm-backend"`),
    - `package_manager` – Package/environment manager (MUST be `"uv"`),
    - `lock_file` – Lock file path (typically `"uv.lock"`),
    - `license` – SPDX license identifier (e.g. `"MIT"`, `"Apache-2.0"`, `"GPL-3.0-or-later"`),
    - `classifiers[]` – PyPI classifiers (e.g. `["Development Status :: 4 - Beta", "Intended Audience :: Science/Research"]`).

  - `User experience & accessibility` – object with:
    - `target_user_technical_level` – Primary user technical level (e.g. `"non-coder"`, `"beginner-coder"`, `"data-scientist"`, `"developer"`),
    - `non_coder_interface_required` – Boolean indicating if package must be usable without coding,
    - `preferred_interface_type[]` – List of interface types (e.g. `["web-app", "gui", "cli-wizard", "notebook"]`),
    - `use_case_complexity` – Complexity level (e.g. `"simple-single-task"`, `"moderate-workflow"`, `"complex-multi-step"`),
    - `default_behavior` – Description of sensible defaults for common use cases,
    - `error_handling_approach` – How errors are presented to users (e.g. `"user-friendly-messages"`, `"technical-debug-info"`).

  - `Observability & logging` – object with:
    - `structured_logging_required` – Boolean (MUST be `true` for research packages),
    - `log_format` – Structured format (MUST include `"jsonl"`),
    - `log_storage_path` – Default runtime log path (e.g. `"logs/"`),
    - `run_log_schema` – Required fields for per-run logs (e.g. `run_id`, `timestamp`, `stage`, `status`, `duration_ms`),
    - `statistics_log_schema` – Required fields for statistical summaries (e.g. metrics, confidence intervals, sample sizes),
    - `retention_policy` – Retention and rotation rules,
    - `pii_redaction_rules` – Rules for redacting sensitive values in logs.

The **Definition of Ready (DoR)** for this proposal is defined in Section 5.

### 2.2 Required outputs (what the blueprint must produce)

Following this blueprint MUST result in:

1. **Agent configuration**
   - `agents.yaml` – Role assignments, tool manifests, and boundaries for the project.

2. **Specification artefacts**
   - `specs/A1.md` – Project & Package Definition.
   - `specs/A2.md` – Features & Public API.
   - `specs/A3.md` – Architecture & Dependencies.
   - `specs/A4.md` – Data Handling & Test Plan.
   - `specs/A5.md` – Quality, CI, and Operations.

3. **Source code & tests**
   - `src/<package_name>/...` – implementation.
   - `tests/` – unit, integration, and acceptance tests.
   - `examples/` – runnable usage examples (scripts/notebooks).

4. **Interactive pipeline**
   - At least one **interactive pipeline entrypoint** (see Section 10), e.g.:
     - CLI wizard (`<pkg>-pipeline`),
     - Notebook-based guided workflow,
     - Simple web UI or TUI that guides the user step-by-step.

5. **Manuscript Artifacts**
   - `manuscript/` directory containing:
     - `artifacts/` – Automatically generated Tables (CSV/LaTeX) and Figures (PNG/PDF).
     - `generation_script.py` (or similar) – The exact code to regenerate all artifacts from raw data.

6. **Governance artefacts**
   - `TRACEABILITY.csv` – Objective/Requirement ↔ Spec ↔ Code ↔ Tests ↔ Source.
   - `DECISIONS.md` – log of key design & implementation decisions.
   - `LITERATURE.bib` – BibTeX references for all DOIs/URLs in the proposal.
   - `REPRODUCIBILITY.md` – how to rebuild, seed, re-run.
   - `preregistration.json` – generated from proposal when `Novelty flag = true`.

6. **Automation & CI**
   - At least one workflow file in `.github/workflows/` (or equivalent) that:
     - Validates specs,
     - Runs tests (including pipeline tests),
     - Runs basic security/dependency checks.

7. **Planning seed artifact** (recommended for document-driven Phase -1)
   - `tasks.seed.yaml` – methodology-derived task seeds generated from `Methodology & Analysis Plan.steps[]`.

8. **Observability artefacts**
   - `logs/` runtime directory (created at run time, excluded from source control).
   - Documented log schemas for run events and statistical summaries.
   - At least one smoke-run log sample generated during validation (when fixture data is available).

### 2.3 Python-specific package outputs

Following this blueprint MUST additionally result in Python-specific artefacts:

1. **Package metadata**
   - `pyproject.toml` – Primary package metadata file (PEP 621 compliant)
     - `[project]` section with name, version, description, authors, dependencies
     - `[build-system]` section specifying build backend
     - `[project.optional-dependencies]` for extras (dev, test, docs, etc.)
     - `[project.scripts]` for console entry points
   - `setup.py` (optional) – Only if backwards compatibility needed
   - `MANIFEST.in` (optional) – For including non-Python files in distributions

2. **Package structure**
   - `src/<package_name>/__init__.py` – Package initialization with version and `__all__`
   - `src/<package_name>/py.typed` – Marker file for PEP 561 type information
   - `src/<package_name>/_version.py` or use `importlib.metadata` for version
   - Follow **src-layout** pattern (recommended) or flat-layout if justified in A3

3. **Dependency specifications**
   - Use `pyproject.toml` `[project.dependencies]` and `[project.optional-dependencies]` as source of truth.
   - Use `uv` dependency groups and locking:
     - `uv add <pkg>` for runtime dependencies
     - `uv add --dev <pkg>` for development dependencies
     - `uv lock` to generate/update `uv.lock`
   - `requirements*.txt` files are optional exports only, not the primary dependency source.

4. **Python environment**
   - `.python-version` – Specifies Python version for pyenv/asdf
   - `runtime.txt` – For deployment platforms (Heroku, etc.)
   - `.tool-versions` (optional) – For asdf version manager

5. **Type checking**
   - `mypy.ini` or `pyproject.toml` `[tool.mypy]` section
   - Type stubs in `<package_name>-stubs/` if needed
   - `py.typed` marker for typed packages (PEP 561)

6. **Code quality configuration**
   - `pyproject.toml` sections for:
     - `[tool.ruff]` – Linting and formatting
     - `[tool.black]` – Code formatting (if using black)
     - `[tool.isort]` – Import sorting (if not using ruff)
     - `[tool.pytest.ini_options]` – Test configuration
     - `[tool.coverage.run]` – Coverage settings
   - `.pre-commit-config.yaml` – Pre-commit hooks configuration

7. **Distribution artefacts** (generated, not in source control)
   - `dist/*.whl` – Built wheel distributions
   - `dist/*.tar.gz` – Source distributions (sdist)
   - Build using `uv build` (PEP 517-compatible frontend)

8. **Observability configuration**
   - Logging module/config in package code (e.g. `src/<package_name>/logging_config.py`)
   - Structured log schema documentation (run log + statistics log fields)
   - Default persisted log paths documented (`logs/runs/`, `logs/stats/` or equivalent)

---

## 3. Roles

Roles are logical; one person (or AI) can hold multiple roles. During Phase 1A, each active role is formally instantiated with a tool manifest.

- **R1 – Orchestrator**  
  Owns the overall process. Accepts/rejects proposals; enforces the blueprint; establishes the agent team.

- **R2 – Architect**  
  Owns A1–A3; defines package boundaries, APIs, and architecture.

- **R3 – Domain Scientist**  
  Owns problem framing, Objectives, and domain-correctness. RESPONSIBLE for the **Methodological Outline** and ensuring algorithms match the research design.

- **R4 – Implementer**  
  Writes the code and tests according to specs and tasks.

- **R5 – Tester**  
  Designs and executes tests; vets coverage and acceptance criteria.

- **R6 – Documenter**  
  Owns documentation, examples, and interactive pipeline UX. RESPONSIBLE for **Manuscript Artifact Generation** (ensuring the package produces the required Tables/Figures).

- **R7 – RPM (Research Product Manager)**  
  Owns traceability, preregistration, reproducibility, and metadata.

Agents and humans SHOULD tag their actions with role IDs for traceability (e.g. comments in `DECISIONS.md` or commit messages).

---

## 4. Specification Artefacts (A1–A5)

These are the **high-level specs** that MUST be produced before serious coding begins.

### 4.1 A1 – Project & Package Definition

Must contain:

- **Package identity**
  - PyPI package name (`pypi_name`) and import name (`import_name`)
  - Short description (one-line, for `pyproject.toml` description field)
  - Long description (for README and PyPI landing page)
  - Package version scheme (semantic versioning recommended: MAJOR.MINOR.PATCH)

- **Python compatibility**
  - Minimum Python version (e.g. `3.9`)
  - Maximum tested Python version
  - `requires-python` specifier (PEP 440 format)
  - Target platforms (Linux, macOS, Windows, or platform-specific)

- **Primary users and use-cases**
  - Target audience (researchers, data scientists, developers, etc.)
  - Typical workflows this package enables
  - Example use-cases with expected inputs/outputs

- **Constraints**
  - Compute requirements (CPU, memory, GPU if applicable)
  - Performance targets (latency, throughput)
  - Data privacy requirements (GDPR, HIPAA, etc.)
  - Dependency constraints (pure Python vs C-extensions)

- **Success criteria**
  - What "done" means for this package
  - Installability: package resolves with `uv sync` and installs cleanly from built distributions
  - Usability: Core workflow completable in < 10 lines of code
  - Quality: Passes all tests, type checks, and linting

- **Alignment with Objectives**
  - Explicit mapping from `proposal.normalized.json` Objectives to package features
  - Cross-references to Objectives by ID

### 4.2 A2 – Features & Public API

Must list every **feature** and **public API function/class** with:

- **ID** (e.g. `FN.001`, `CLASS.001`, `PIPELINE.CLI.001`)

- **Python signature with type hints** (PEP 484, 586, 604)
  - Function/method name following PEP 8 conventions (`snake_case`)
  - Class names in `PascalCase`
  - Full type annotations for parameters and return values
  - Use of `typing` module constructs (`Optional`, `Union`, `Literal`, `TypeVar`, etc.)
  - Example: `def process_data(data: pd.DataFrame, method: Literal["pls", "pca"] = "pls") -> np.ndarray:`

- **Docstring format**
  - Choose one style consistently: Google, NumPy, or Sphinx (reST)
  - Include: brief description, parameters, returns, raises, examples
  - Example (Google style):
    ```python
    """Process input data using the specified method.

    Args:
        data: Input DataFrame with features in columns
        method: Algorithm to use, either "pls" or "pca"

    Returns:
        Transformed data as numpy array

    Raises:
        ValueError: If method is not recognized

    Examples:
        >>> result = process_data(df, method="pls")
    """
    ```

- **Behaviour description**
  - Clear explanation of what the function/class does
  - Any side effects or state changes
  - Performance characteristics (if relevant)

- **Module placement**
  - Which module the function/class belongs to (e.g. `<package>.preprocessing`, `<package>.models`)
  - Whether it's exported in `__init__.py` (part of public API)

- **Reference to Objectives and source DOIs**
  - Links back to proposal Objectives
  - Citations to papers/references if implementing published algorithms

A2 **must include** at least one **Interactive Pipeline feature** (see Section 10).

### 4.3 A3 – Architecture & Dependencies

Must:

- **Package structure and layout**
  - Choice: `src/` layout (recommended) or flat layout with justification
  - Module hierarchy and organization
  - Example structure:
    ```
    project_root/
    ├── src/
    │   └── package_name/
    │       ├── __init__.py
    │       ├── _version.py
    │       ├── py.typed
    │       ├── core/
    │       ├── models/
    │       ├── utils/
    │       └── cli/
    ├── tests/
    ├── docs/
    ├── examples/
    └── pyproject.toml
    ```

- **Module boundaries**
  - **Public API**: Functions/classes exported in `__init__.py` and documented
  - **Internal/Private**: Modules prefixed with `_` (e.g. `_internal.py`)
  - `__all__` definition in each module to control `from module import *`
  - Clear documentation of what users should import vs. internal implementation

- **Python dependencies**
  - **Core dependencies** with version constraints (PEP 440 specifiers)
    - Use `>=` for minimum versions, `<` for exclusions
    - Example: `numpy>=1.20,<2.0`, `pandas>=1.3`
    - Rationale for each dependency
  - **Optional dependencies** grouped by purpose
    - `dev`: Development tools (ruff, mypy, pre-commit)
    - `test`: Testing tools (pytest, pytest-cov, hypothesis)
    - `docs`: Documentation tools (sphinx, sphinx-rtd-theme)
    - Domain-specific extras (e.g. `gpu`, `viz`, `extra-formats`)
  - **Python version compatibility**
    - Explicit statement of supported Python versions
    - Any version-specific code paths or compatibility shims

- **Object-Oriented Architecture patterns**

  Python packages SHOULD use object-oriented design:

  - **Core domain classes**
    - Identify main business objects (e.g., `Dataset`, `Model`, `Pipeline`, `Result`)
    - Define class hierarchies using inheritance
    - Example hierarchy:
      ```
      BaseModel (ABC)
      ├── RegressionModel (ABC)
      │   ├── PLSModel
      │   └── PCRModel
      └── ClassificationModel (ABC)
          └── PLSDAModel
      ```

  - **Design patterns used**
    - **Factory Pattern**: For creating model instances
      ```python
      model = ModelFactory.create("pls", n_components=3)
      ```
    - **Strategy Pattern**: For interchangeable algorithms
    - **Observer Pattern**: For progress callbacks
    - **Builder Pattern**: For complex object construction (fluent API)
    - **Template Method**: For defining algorithm skeletons in base classes

  - **Composition over inheritance**
    - How objects are composed from simpler components
    - Dependency injection for flexibility
    - Example: `Pipeline` composed of `Preprocessor + Model + Validator`

  - **Overall architecture**
    - Layered architecture: presentation → business logic → data access
    - Modular design with clear separation of concerns
    - State management: where is state stored (in objects, passed as parameters, etc.)
    - Extension points: abstract base classes, hooks, plugin interfaces
    - Observability layer: centralized logging/timing/stats emitters shared across modules

- **Interactive pipeline integration**
  - How CLI/notebook/web components interface with core logic
  - Separation of presentation layer from business logic
  - Configuration and parameter passing mechanisms
  - Dedicated manuscript artifact layer (tables/plots) separated from model training code

### 4.4 A4 – Data Handling & Test Plan

Must:

- **Dataset specifications**
  - Describe each dataset from the proposal
  - How each dataset is loaded, validated, and used
  - Data format expectations (CSV, HDF5, Parquet, etc.)
  - Schema validation approach (pandera, pydantic, custom)

- **Test fixtures (pytest)**
  - `conftest.py` organization (global vs. per-module)
  - Fixture definitions with appropriate scopes (`function`, `module`, `session`)
  - Synthetic data generators for testing
  - Example:
    ```python
    @pytest.fixture(scope="module")
    def sample_dataset():
        """Generate synthetic test data."""
        return pd.DataFrame(...)
    ```

- **Test organization**
  - Mirror source structure: `tests/test_<module>.py` for each `src/<package>/<module>.py`
  - Separate directories for unit, integration, and acceptance tests if needed
  - Test file naming: `test_*.py` or `*_test.py`
  - Test function naming: `test_<function_name>_<scenario>` (PEP 8)

- **Test matrix**
  - **Unit tests** (per function/class)
    - Test each public function in isolation
    - Mock external dependencies
    - Cover edge cases, error conditions, type validation
    - Parametrized tests using `@pytest.mark.parametrize`

  - **Integration tests** (per feature)
    - Test combinations of functions working together
    - Test with realistic data flows
    - Verify feature-level behavior from A2

  - **Acceptance tests** (mapped to Objectives)
    - Each Objective must have at least one acceptance test
    - Tests verify success criteria from proposal
    - End-to-end validation of research claims

  - **Interactive pipeline tests**
    - CLI tests using subprocess or click.testing.CliRunner
    - Notebook execution tests (using nbmake or papermill)
    - Headless mode tests for web/TUI interfaces
    - Manuscript artifact mechanism tests (manifest coverage + callable generators for all required tables/figures)
    - Publication plot checks (file format, minimum DPI, deterministic output paths) in smoke/integration runs
    - Logging mechanism tests (run logs and statistics logs are persisted with required schema fields)

- **Test markers and organization**
  - Use `@pytest.mark` for categorization:
    - `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.acceptance`
    - `@pytest.mark.slow` for long-running tests
    - `@pytest.mark.gpu` for GPU-dependent tests
  - Configure markers in `pyproject.toml` `[tool.pytest.ini_options]`

- **Coverage requirements**
  - Minimum coverage thresholds (specified in A5)
  - Coverage measurement using `pytest-cov`
  - Branch coverage vs. line coverage
  - Exclusions for deliberate untested code (`# pragma: no cover`)

### 4.5 A5 – Quality, CI, and Operations

Must:

- **Code quality tools and standards**
  - **Reuse-before-build principle (MANDATORY)**
    - Do NOT build custom components from scratch when a well-supported library already provides equivalent functionality.
    - If custom implementation is chosen, A3/A5 MUST document why existing library components were insufficient.
    - Preference order: standard library → established third-party library → custom implementation.

  - **No redundancy principle (MANDATORY)**
    - Do NOT pollute the codebase with duplicate, dead, or functionally redundant code paths.
    - Shared behavior MUST be centralized in reusable modules/functions/classes.
    - A5 MUST include duplicate-code checks and refactoring expectations during review.

  - **Linting**: ruff (recommended), flake8, or pylint
    - Specify rule sets enabled/disabled
    - PEP 8 compliance level
    - Configuration in `pyproject.toml` `[tool.ruff]` or `[tool.flake8]`

  - **Formatting**: ruff format or black
    - Line length (typically 88 or 100)
    - String quote style
    - Configuration in `pyproject.toml` `[tool.ruff.format]` or `[tool.black]`

  - **Import sorting**: ruff (built-in) or isort
    - Import grouping style (stdlib, third-party, first-party)
    - Configuration in `pyproject.toml`

  - **Type checking**: mypy (primary) or pyright
    - Strictness level: `--strict`, or specific options
    - Configuration in `pyproject.toml` `[tool.mypy]`
    - Inline type ignore policy (`# type: ignore[specific-error]`)

- **Testing standards**
  - **Framework**: pytest with plugins
    - `pytest-cov` for coverage
    - `pytest-xdist` for parallel execution
    - `pytest-mock` for mocking
    - Others as needed (pytest-timeout, pytest-benchmark)

  - **Coverage thresholds**
    - Minimum line coverage (e.g. 80%, 90%)
    - Minimum branch coverage (if applicable)
    - Per-file coverage requirements
    - Configuration in `pyproject.toml` `[tool.coverage.run]` and `[tool.coverage.report]`

  - **Test execution**
    - Command: `pytest tests/` or `python -m pytest`
    - Coverage command: `pytest --cov=<package> --cov-report=term --cov-report=html`
    - Parallel execution: `pytest -n auto` (with pytest-xdist)

- **Observability and logging standards**
  - Structured runtime logging is mandatory for analysis and pipeline execution.
  - Logs MUST be persisted to disk (default `logs/`) and include stable `run_id` correlation.
  - Runtime event logs SHOULD use JSON Lines (`*.jsonl`) with fields such as:
    - `run_id`, `timestamp`, `stage`, `event`, `status`, `duration_ms`, `component`
  - Statistical logs MUST be persisted separately (for example `logs/stats/<run_id>.json`) and include:
    - key metrics, sample sizes, uncertainty summaries, and provenance/version metadata
  - Logging configuration MUST be centralized and configurable (path, level, retention, redaction).
  - Sensitive fields MUST be redacted according to `pii_redaction_rules`.
  - A5 MUST define logging validation tests and failure criteria.

- **Pre-commit hooks**
  - `.pre-commit-config.yaml` with:
    - Trailing whitespace removal
    - End-of-file fixer
    - YAML/JSON validation
    - Ruff linting and formatting
    - mypy type checking
    - pytest (fast tests only)

- **Continuous Integration (CI)**
  - **Platform**: GitHub Actions (recommended), GitLab CI, or CircleCI
  - **Matrix testing**:
    - Multiple Python versions (e.g. 3.9, 3.10, 3.11, 3.12)
    - Multiple OS if applicable (Ubuntu, macOS, Windows)
  - **CI checks** (run on every push/PR):
    1. Sync environment: `uv sync --group dev --group test`
    2. Linting: `ruff check .`
    3. Formatting check: `ruff format --check .`
    4. Type checking: `uv run mypy src/<package>`
    5. Tests: `uv run pytest tests/ --cov=<package> --cov-report=xml`
    6. Logging mechanism tests: run/validate persisted runtime + statistics logs
    7. Coverage enforcement: fail if below threshold
    8. Build check: `uv build`
    9. Security scan: `uvx pip-audit` or `uvx safety check`
  - **Workflow artifacts**:
    - Coverage reports (upload to codecov/coveralls)
    - Built distributions (wheel and sdist)
    - Test results (JUnit XML)

- **Documentation builds**
  - Sphinx documentation built in CI
  - Doctests executed: `pytest --doctest-modules src/`
  - Link checking: `sphinx-build -b linkcheck`
  - Deploy to ReadTheDocs or GitHub Pages

- **Reproducibility requirements**
  - Lock files for exact reproduction
    - `uv.lock` (required)
    - Generated from dependencies declared in `pyproject.toml`
  - Environment specification
    - Python version in `.python-version` or documented
    - System dependencies (if any) documented in README
  - Seed handling for stochastic components
    - Random seed setting utilities
    - Documentation of seed usage in tests and examples

- **Release and versioning**
  - Version source of truth: `_version.py` or `pyproject.toml` with dynamic versioning
  - Changelog maintenance (Keep a Changelog format)
  - Git tagging strategy (e.g. `v1.0.0`)
  - PyPI publishing workflow (manual or automated via CI; `uv publish` or `uvx twine upload`)

- **Support and maintenance**
  - Support level: active development, maintenance mode, or unsupported
  - Issue tracker and contribution guidelines
  - Security policy (SECURITY.md) if applicable
  - Deprecation policy for breaking changes

- **Performance and scalability engineering**
  - Define performance budgets in A3/A5 (runtime, memory, and dataset-size targets).
  - Document algorithmic complexity for core paths (Big-O for fit/predict and pipeline stages).
  - Specify parallelism model (`pytest-xdist`, multiprocessing, threading, or async I/O) with rationale.
  - Use vectorized operations and batch processing for large datasets; avoid row-wise Python loops in hot paths.
  - Add caching/checkpoint strategy for expensive intermediate computations in pipelines.
  - Add memory controls (chunked I/O, streaming readers, and explicit limits for large artifacts).
  - Add profiling and benchmark tasks (`pytest-benchmark` or equivalent) and store baseline results.
  - Add structured logging and timing hooks so slow stages are measurable in CI and production runs.

### 4.6 A6 – User Experience (UX) & Non-Coder Accessibility (NEW)

This specification defines how the package ensures usability for non-programmers and follows OO design principles.

Must contain:

- **Target User Profiles**
  - **Primary user type**: Non-coder, beginner coder, data scientist, or developer
  - **User personas**: Describe 2-3 typical users with their goals and pain points
  - **Technical skill assumptions**: What users are expected to know
  - **What users should NOT need to know**: (e.g., "Users should not need to understand Python syntax")

- **Object-Oriented Design Patterns**

  Python is object-oriented; the package SHOULD demonstrate OO principles:

  - **Core Classes and Objects**
    - Identify main domain objects (e.g., `Model`, `Dataset`, `Pipeline`, `Result`)
    - Class hierarchy and inheritance relationships
    - Use of abstract base classes (ABC) for extensibility
    - Example:
      ```python
      from abc import ABC, abstractmethod

      class BaseModel(ABC):
          """Abstract base class for all models."""

          @abstractmethod
          def fit(self, X, y):
              """Fit the model to training data."""
              pass

          @abstractmethod
          def predict(self, X):
              """Make predictions on new data."""
              pass

      class PLSModel(BaseModel):
          """Partial Least Squares model implementation."""

          def fit(self, X, y):
              # Implementation
              pass

          def predict(self, X):
              # Implementation
              pass
      ```

  - **Encapsulation**
    - Public vs. private attributes (using `_` prefix convention)
    - Properties (`@property`) for controlled access
    - Data validation in setters
    - Example:
      ```python
      class Dataset:
          def __init__(self, data):
              self._data = None
              self.data = data  # Uses setter for validation

          @property
          def data(self):
              return self._data

          @setter
          def data(self, value):
              if value is None:
                  raise ValueError("Data cannot be None")
              self._data = value
      ```

  - **Composition over Inheritance**
    - How objects are composed from simpler components
    - Dependency injection patterns
    - Example:
      ```python
      class Pipeline:
          def __init__(self, preprocessor, model, postprocessor):
              self.preprocessor = preprocessor
              self.model = model
              self.postprocessor = postprocessor

          def run(self, data):
              processed = self.preprocessor.transform(data)
              predictions = self.model.predict(processed)
              return self.postprocessor.format(predictions)
      ```

  - **Polymorphism**
    - Use of common interfaces across different implementations
    - Duck typing where appropriate
    - Example: Multiple model types with same `fit/predict` interface

- **Non-Coder Interface Requirements**

  If `non_coder_interface_required = true`, the package MUST provide:

  - **Pythonic Interactive Console Interface** (PRIMARY REQUIREMENT):

    The package MUST provide an **interactive terminal/console experience** where non-coders can type simple, readable commands with minimal syntax.

    **Key principles** (Python-first):
    - Short, memorable function names (`read()`, `plot()`, `summary()`)
    - Pipe-able operations (method chaining)
    - Sensible defaults for everything
    - Rich terminal output (tables, formatted text)
    - Interactive plots that open in separate windows
    - No complex syntax required

    **Example terminal session**:
    ```python
    # In Python terminal or IPython
    >>> import mytool as mt

    >>> # Load data
    >>> data = mt.read("data.csv")
    Loaded 100 samples with 10 features

    >>> # Quick look at data
    >>> data.head()
       Feature1  Feature2  Feature3  ...
    0      1.2      3.4      5.6  ...
    1      2.3      4.5      6.7  ...
    ...

    >>> # Analyze
    >>> model = mt.pls(data, target="Y", n_components=3)
    Building PLS model...
    R² = 0.85, Q² = 0.78
    Model ready!

    >>> # Summary (like R's summary())
    >>> model.summary()
    ╭─────────────────────────────────────╮
    │ PLS Model Summary                   │
    ├─────────────────────────────────────┤
    │ Components:        3                │
    │ R² (calibration):  0.85             │
    │ Q² (CV):           0.78             │
    │ RMSEC:             0.34             │
    │ RMSECV:            0.41             │
    ╰─────────────────────────────────────╯

    >>> # Plot (like R's plot())
    >>> model.plot()  # Opens interactive plot window
    Displaying scores plot...

    >>> # Predict new data
    >>> predictions = model.predict("new_data.csv")
    >>> predictions.save("results.csv")
    Saved predictions to results.csv
    ```

    **Implementation requirements**:

    1. **IPython/Jupyter integration**
       - Rich display in IPython console
       - HTML tables in Jupyter notebooks
       - Inline plots when possible
       - Tab completion for all methods

    2. **Readable method names** (Python-first)
      - `load()` or `read()` instead of `read_csv_with_validation()`
      - `fit()` or `build()` instead of `fit_transform_model()`
      - `plot()` instead of `generate_visualization()`
      - `summary()` for model summaries

    3. **Method chaining** (fluent interface)
       ```python
       # Fluent interface pattern
       result = (mt.read("data.csv")
                   .clean()
                   .scale()
                   .pls(target="Y")
                   .plot())
       ```

    4. **Rich terminal output** (using `rich` or `prettytable`)
       - Formatted tables (not raw numpy arrays)
       - Color-coded output
       - Progress bars for long operations
       - Clear status messages

    5. **Interactive prompts** (when needed)
       ```python
       >>> model.tune()  # Auto-prompts for parameters
       Number of components? [auto]: <press enter for auto>
       Cross-validation folds? [10]: <press enter for default>
       Tuning model...
       ```

    6. **Help system** (like R's `?function`)
       ```python
       >>> mt.help("pls")  # Or just ?mt.pls in IPython
       # Shows clear documentation with examples
       ```

  - **Minimal-Code Interface** (for beginner coders):
    - **One-liner workflows** for common tasks
      ```python
      # Users can copy-paste this single line
      result = mytool.quick_analysis("data.csv", method="pls")
      ```

    - **Fluent/Builder pattern** for readable workflows
      ```python
      # Readable, self-documenting API
      analysis = (MyTool()
                   .load_data("data.csv")
                   .preprocess()
                   .analyze(method="pls")
                   .visualize()
                   .save("results/"))
      ```

    - **Configuration files** for reproducible runs
      ```python
      # Users edit YAML, don't write code
      mytool.run_from_config("my_analysis.yaml")
      ```

- **Sensible Defaults**

  For every feature with parameters, define:

  - **Default parameter values** that work for 80% of use cases
  - **Auto-detection** where possible (e.g., infer data types, suggest optimal parameters)
  - **Explanation** of what defaults mean and when to change them
  - Example:
    ```python
    def analyze(data,
                method="pls",  # Most common method
                n_components="auto",  # Automatically determined
                scaling=True,  # Usually needed
                validation="cv"):  # Cross-validation by default
        """
        Analyze data using multivariate methods.

        Defaults are chosen for typical use cases. Override only if needed.

        Args:
            method: "pls" works for most regression tasks
            n_components: "auto" selects based on explained variance
            scaling: True recommended unless data already scaled
            validation: "cv" provides robust error estimates
        """
        pass
    ```

- **Error Handling for Non-Coders**

  - **User-friendly error messages**
    ```python
    # BAD (technical jargon)
    raise ValueError("Invalid shape (100, 5), expected (n, 10)")

    # GOOD (explains problem and solution)
    raise ValueError(
        "Your data has 5 columns, but this model expects 10 features.\n"
        "This usually means:\n"
        "  1. You're using data from a different source, or\n"
        "  2. Some preprocessing steps were skipped.\n"
        "Try running: mytool.check_data('data.csv') for diagnostics."
    )
    ```

  - **Error recovery suggestions**
    - Suggest what user should do next
    - Link to relevant documentation
    - Provide diagnostic commands

  - **Validation before execution**
    - Check inputs before long computations
    - Warn about potential issues (e.g., "Your dataset is very small")
    - Confirm destructive operations

- **Progressive Disclosure**

  - **Simple by default, powerful when needed**
    - Basic API for common tasks (high-level functions)
    - Advanced API for custom workflows (class-based)
    - Expert API for research/extension (low-level functions)

  - **Example**:
    ```python
    # LEVEL 1: Simple function for non-coders
    result = mytool.analyze_csv("data.csv")

    # LEVEL 2: Class-based API for more control
    pipeline = Pipeline()
    pipeline.load("data.csv")
    pipeline.preprocess(method="standard")
    pipeline.fit(algorithm="pls", components=5)
    result = pipeline.predict(new_data)

    # LEVEL 3: Expert API for custom implementations
    from mytool.core import PLSRegressor
    from mytool.preprocessing import CustomScaler

    scaler = CustomScaler(strategy="robust")
    model = PLSRegressor(n_components=5, scale=False)
    X_scaled = scaler.fit_transform(X)
    model.fit(X_scaled, y)
    ```

- **Documentation for Non-Coders**

  - **Video tutorials** (or links to them)
  - **Screenshot-based guides** for GUI/web interfaces
  - **Cookbook-style examples** with copy-paste code
  - **Troubleshooting FAQ** for common errors
  - **Glossary** of technical terms
  - **"What do I do first?"** quick-start guide

- **Validation & Testing**

  - **Usability testing** with target users (if possible)
  - **Example success criteria**:
    - "A domain scientist can complete basic analysis in < 5 minutes without reading docs"
    - "Non-coder can use web interface with zero Python knowledge"
    - "Error messages tested for comprehension by non-programmers"

---

## 5. Standardising the Proposal (When It's Ready for AI)

This section describes **when a proposal is "standardised" and ready** so that you can simply ask an AI:

> "Read `proposal.normalized.json` and `BLUEPRINT-Universal-1.1.md` and start working."

### 5.1 Standardisation workflow (human or AI-assisted)

A proposal is considered **standardised** when all the following are true:

1. **Proposal file exists**
   - There is a single file named `proposal.normalized.json` at the root of the project (or clearly pointed to).

2. **Schema is respected**
   - The file matches the required fields in Section 2.1 (Title, Scope, Objectives, Data, etc.).

3. **Fields are concrete**
   - Title is specific (not generic).
   - Scope clearly says what is in and out.
   - Each Objective:
     - Is testable,
     - Has an `owner`,
     - Has an `acceptance` ID,
     - Has `provenance.doi` if applicable.
   - All datasets have:
     - Real URLs (no placeholders),
     - Stated licenses,
     - `pii_classification`.

4. **Novelty & preregistration**
   - If `Novelty flag = true`, there is a valid `Preregistration URL` or a plan to generate one.

5. **Risks & mitigations**
   - Each risk:
     - Is clearly described,
     - Has an `owner`,
     - Has a `verification_method` that is objectively checkable.

6. **Observability & logging profile**
   - `Observability & logging` is present.
   - `structured_logging_required = true`.
   - Run-level and statistics-level logging schemas are defined.

### 5.2 Formal Definition of Ready (DoR)

Before any substantial code is written, the **proposal** must pass DoR.

The Orchestrator (R1) MUST verify:

1. **Schema validity**
   - `proposal.normalized.json` matches the agreed JSON Schema (no required fields missing).

2. **No placeholders**
   - No occurrences of strings like `"TBD"`, `"???"`, `"REPLACE-ME"` in:
     - `Title`, `Scope`, `Objectives[*].statement`, `Risks[*].risk`, or critical data fields.

3. **Data availability**
   - Every dataset URL is reachable (HTTP 200).
   - Licenses are compatible with the intended use.
   - PII classification is explicitly stated (e.g. `NONE`, `LOW`, `HIGH`).

4. **Novelty & preregistration**
   - If `Novelty flag = true`, `Preregistration URL` must be present and parsable.
   - If prereg is not yet final, R7 MUST at least generate a draft `preregistration.json` based on the proposal.

5. **Objectives & Risks cross-check**
   - Each Objective has:
     - A unique `acceptance` ID,
     - A named `owner`.
   - Each Risk has a `verification_method` that is clear and testable.

6. **Observability & logging completeness**
   - `Observability & logging` exists with required fields.
   - Structured log format and storage path are specified.
   - `run_log_schema` and `statistics_log_schema` are non-empty and testable.

If any condition fails, the Orchestrator returns the proposal for revision and **halts implementation**.

Once all criteria are satisfied, the proposal is **standardised** and AI can safely start Phase 1A.

### 5.3 Phase -1: Proposal Standardisation by Three-Expert Panel (Optional but Recommended)

This subsection defines how AI agents can transform an unstructured proposal (e.g. DOCX, PDF, free text) into a standardised `proposal.normalized.json` using a **three-member expert panel**.

#### 5.3.1 Purpose

The goal is to allow a user to simply provide:

- One or more unstructured proposal documents (e.g. `Goal.docx`, manuscript outline, notes), and
- This blueprint (`BLUEPRINT-Universal-1.1.md`),

and then instruct an AI system:

> "Read the proposal documents and `BLUEPRINT-Universal-1.1.md`, standardise the proposal into `proposal.normalized.json`, verify DoR, and then start implementing."

#### 5.3.2 Roles in the three-expert panel

Define three domain-expert agents:

- **E1 – Expert 1 (Domain Perspective A)**
- **E2 – Expert 2 (Domain Perspective B)**
- **E3 – Expert 3 (Method/Stats Perspective)**

All three act under role **R3 – Domain Scientist**, but with slightly different emphasis (e.g. application side vs. methodological side).

An additional AI agent acts as **R1 – Orchestrator** for this phase.

#### 5.3.3 Inputs to the panel

The panel receives:

- The unstructured proposal documents (e.g. `.docx`, `.pdf`, `.md`),
- Any prior notes from the human proposer,
- This blueprint file (`BLUEPRINT-Universal-1.1.md`).

They do **not** assume `proposal.normalized.json` exists yet.

#### 5.3.4 Procedure (Phase -1 workflow)

The Orchestrator (R1) MUST run the following steps:

1. **Independent draft stage**
   - E1, E2, and E3 **independently** read the unstructured proposal and blueprint.
   - Each expert produces a full candidate `proposal.normalized.json` that:
     - Follows the structure in Section 2.1,
     - Fills Title, Scope, Objectives, Data, Novelty flag, Risks, etc.,
     - Avoids obvious placeholders (`TBD`, `???`, `REPLACE-ME`).
   - Each expert also writes a short rationale (1–2 paragraphs) for any non-trivial interpretation or assumption.

2. **Merge & comparison stage**
   - R1 collects the three candidate JSON files: `proposal_E1.json`, `proposal_E2.json`, `proposal_E3.json`.
   - For each top-level field and important sub-field (Title, Scope, each Objective, each Dataset, each Risk), R1 compares the three values:
     - If **all three agree** → accept that value directly.
     - If **two agree, one differs** → adopt the majority value and record the disagreement + rationale in `DECISIONS.md`.
     - If **all three differ** → mark this field as "contested" and send it to the **deliberation round**.

3. **Deliberation round for contested fields**
   - For each contested field:
     - R1 asks E1, E2, and E3 to each briefly justify their version (1–3 sentences).
     - R1 summarises the three justifications and:
       - Either selects one version (stating why in `DECISIONS.md`), or
       - Synthesises a new combined value that addresses the strongest arguments.
     - If still ambiguous, R1 SHOULD flag this field as needing **human confirmation** and mark it with a temporary tag (e.g. `"NEEDS-HUMAN-REVIEW"`).

4. **Produce a unified `proposal.normalized.json`**
   - R1 builds the unified proposal by:
     - Taking agreed/majority values for non-contested fields,
     - Using the chosen/synthesised values for contested fields,
     - Ensuring the JSON matches the structure in Section 2.1.
   - Any `"NEEDS-HUMAN-REVIEW"` tags MUST be clearly visible and listed in `DECISIONS.md`.

5. **Human confirmation (optional but recommended)**
   - If a human proposer is available:
     - Present the unified JSON and any `"NEEDS-HUMAN-REVIEW"` items.
     - Incorporate their corrections/decisions.
   - Remove all `"NEEDS-HUMAN-REVIEW"` tags once resolved.

6. **Run DoR (Definition of Ready) checks**
   - Once the unified `proposal.normalized.json` is produced, R1 runs the DoR checks in Section 5.2.
   - If DoR fails:
     - R1 MUST generate a **validation report** describing:
       - Which fields violate schema or readiness rules,
       - Suggested fixes from the panel.
     - The proposal is **not yet standardised**; panel or human must revise and repeat this phase.
   - If DoR passes:
     - The proposal is **standardised and ready**.
     - The file is saved as the canonical `proposal.normalized.json`.

#### 5.3.5 Output of the panel

At the end of Phase -1, the system MUST produce:

1. `proposal.normalized.json` – unified, standardised, DoR-compliant.
2. Optional individual drafts: `proposal_E1.json`, `proposal_E2.json`, `proposal_E3.json` (for audit).
3. Entries in `DECISIONS.md` documenting:
   - Major disagreements and how they were resolved,
   - Any fields where human confirmation was required.
4. Recommended companion planning artifact: `tasks.seed.yaml` generated from `Methodology & Analysis Plan.steps[]`.

Once these artefacts exist and DoR is passed, the AI Orchestrator (R1) MAY proceed to **PHASE 0 – READ_PROPOSAL** and then through PHASES 1A–6 as defined in Section 8.

#### 5.3.6 Document-driven normalisation contract (for 3-file prompts)

When users provide three source documents (Concept/Idea, Manuscript Outline, Literature Notes), R1 and the expert panel MUST apply this contract:

1. **Extract & map**
   - Concept/Idea file populates `Title`, `Scope`, core `Objectives[]`, novelty, and risks.
   - Manuscript Outline populates `Methodology & Analysis Plan.steps[]` and `manuscript_requirements`.
   - Literature Notes populate `literature_context.provided_notes` and `literature_context.key_references[]`.

2. **Algorithm detail expansion**
   - Every ordered methodology step from the outline MUST appear as a concrete entry in `Methodology & Analysis Plan.steps[]`.
   - Each methodology step MUST be mirrored in `tasks.seed.yaml` as at least one implementation/testing task seed with owner and expected validation hook.

3. **Artifact definition completeness**
   - Every table and figure named in the outline MUST be listed in `manuscript_requirements.tables[]` and `manuscript_requirements.figures[]`.
   - Missing artifact names MUST be flagged as contested fields, not silently dropped.

4. **Governance readiness**
   - `literature_context` MUST include enough raw notes + structured references for R7 to generate `LITERATURE.bib` without re-reading source documents.

5. **Validation gate**
   - Phase -1 is not complete if methodology steps are missing task seeds or if manuscript artifacts are only partially mapped.

---

## 6. Agent Establishment (Phase 1A Foundation)

This section defines **how to establish the agent team** before any specification or implementation work begins. This is the foundation that makes everything else possible.

### 6.1 Why agent establishment matters

Without explicit agent establishment:

- Roles remain abstract concepts rather than configured workers
- Tool access is undefined, leading to scope creep or capability gaps
- Handoffs between agents lack structure
- Violations of role boundaries go undetected
- Traceability from artifact to producer is incomplete

Phase 1A solves these problems by formally instantiating each agent with defined capabilities.

### 6.2 Agent configuration schema (`agents.yaml`)

The Orchestrator (R1) MUST produce an `agents.yaml` file with the following structure:

```yaml
# agents.yaml - Agent Team Configuration
# Generated during Phase 1A by R1 (Orchestrator)

meta:
  blueprint_version: "1.1"
  project_name: "<from proposal.normalized.json>"
  generated_at: "<ISO 8601 timestamp>"
  generated_by: "R1"

team_composition:
  # Which roles are active for this project
  active_roles:
    - R1
    - R2
    - R3
    - R4
    - R5
    - R6
    - R7
  
  # Roles intentionally excluded (with justification)
  excluded_roles: []

agents:
  R1:
    name: "Orchestrator"
    status: "active"
    responsibilities:
      - "Enforce blueprint phases and invariants"
      - "Coordinate handoffs between agents"
      - "Maintain DECISIONS.md"
      - "Validate phase exit criteria"
    tools:
      - tool_id: "phase_controller"
        description: "Advance or block phase transitions"
        permissions: ["read", "write"]
      - tool_id: "decision_logger"
        description: "Append entries to DECISIONS.md"
        permissions: ["write"]
      - tool_id: "validation_runner"
        description: "Execute DoR and phase exit checks"
        permissions: ["execute"]
      - tool_id: "agent_coordinator"
        description: "Assign tasks and request work from other agents"
        permissions: ["read", "write"]
    boundaries:
      - "MUST NOT write spec content (delegate to R2/R3)"
      - "MUST NOT write implementation code (delegate to R4)"
      - "MUST NOT run tests (delegate to R5)"
    success_criteria:
      - "All phases complete in order"
      - "No invariant violations in DECISIONS.md"
      - "All agent handoffs logged"

  R2:
    name: "Architect"
    status: "active"
    responsibilities:
      - "Author A1, A2, A3 specifications"
      - "Define public API signatures"
      - "Resolve architectural decisions"
      - "Ensure spec consistency"
    tools:
      - tool_id: "spec_generator"
        description: "Create and modify A1-A3 markdown files"
        permissions: ["read", "write"]
        target_files: ["specs/A1.md", "specs/A2.md", "specs/A3.md"]
      - tool_id: "schema_validator"
        description: "Validate spec structure against templates"
        permissions: ["execute"]
      - tool_id: "dependency_resolver"
        description: "Analyze and document package dependencies"
        permissions: ["read", "execute"]
      - tool_id: "api_designer"
        description: "Generate API signatures and type definitions"
        permissions: ["read", "write"]
    boundaries:
      - "MUST NOT modify A4 or A5 without R3/R5 approval"
      - "MUST NOT write implementation code"
      - "MUST consult R3 for domain-specific design choices"
    success_criteria:
      - "A1-A3 complete with no TBDs"
      - "Every Objective mapped to at least one A2 feature"
      - "All API signatures have types and descriptions"

  R3:
    name: "Domain Scientist"
    status: "active"
    responsibilities:
      - "Validate scientific correctness of Objectives"
      - "Review A2 features for domain appropriateness"
      - "Define acceptance criteria for Objectives"
      - "Verify dataset suitability"
    tools:
      - tool_id: "literature_fetcher"
        description: "Retrieve and parse DOI references"
        permissions: ["read", "execute"]
      - tool_id: "domain_validator"
        description: "Check scientific claims against literature"
        permissions: ["read"]
      - tool_id: "metric_checker"
        description: "Validate proposed metrics and thresholds"
        permissions: ["read", "execute"]
      - tool_id: "provenance_linker"
        description: "Connect features to source DOIs"
        permissions: ["read", "write"]
    boundaries:
      - "MUST NOT define API signatures (advise R2 instead)"
      - "MUST NOT write implementation code"
      - "MUST escalate architectural decisions to R2"
    success_criteria:
      - "All Objectives scientifically valid"
      - "Acceptance criteria are measurable"
      - "Dataset justifications documented"

  R4:
    name: "Implementer"
    status: "active"
    responsibilities:
      - "Write source code matching A2 signatures"
      - "Create unit test stubs from A4"
      - "Follow architectural patterns from A3"
      - "Maintain code quality per A5"
    tools:
      - tool_id: "code_generator"
        description: "Create source files in src/"
        permissions: ["read", "write"]
        target_dirs: ["src/"]
      - tool_id: "file_writer"
        description: "Create and modify code files"
        permissions: ["read", "write"]
      - tool_id: "linter"
        description: "Run linting checks on code"
        permissions: ["execute"]
      - tool_id: "formatter"
        description: "Apply code formatting"
        permissions: ["execute"]
      - tool_id: "test_stub_creator"
        description: "Generate test file skeletons from A4"
        permissions: ["read", "write"]
        target_dirs: ["tests/"]
    boundaries:
      - "MUST NOT modify specs (A1-A5)"
      - "MUST NOT modify agents.yaml"
      - "MUST follow A2 signatures exactly"
      - "MUST request spec clarification via DECISIONS.md if ambiguous"
    success_criteria:
      - "All A2 features implemented"
      - "Code passes linting"
      - "Test stubs exist for all expected_tests"

  R5:
    name: "Tester"
    status: "active"
    responsibilities:
      - "Execute test suites"
      - "Validate coverage thresholds"
      - "Report test failures with diagnostics"
      - "Verify acceptance criteria"
    tools:
      - tool_id: "test_runner"
        description: "Execute pytest/unittest suites"
        permissions: ["execute"]
      - tool_id: "coverage_analyzer"
        description: "Measure and report code coverage"
        permissions: ["execute", "read"]
      - tool_id: "fixture_generator"
        description: "Create test fixtures from A4 specs"
        permissions: ["read", "write"]
        target_dirs: ["tests/fixtures/"]
      - tool_id: "assertion_builder"
        description: "Generate assertion code from acceptance criteria"
        permissions: ["read", "write"]
    boundaries:
      - "MUST NOT modify source code in src/"
      - "MUST NOT modify specs"
      - "MUST escalate spec errors to R2/R3 via DECISIONS.md"
    success_criteria:
      - "All expected_tests pass"
      - "Coverage meets A5 thresholds"
      - "Acceptance tests verify all Objectives"

  R6:
    name: "Documenter"
    status: "active"
    responsibilities:
      - "Write user-facing documentation"
      - "Create runnable examples"
      - "Document interactive pipeline usage"
      - "Maintain README and guides"
    tools:
      - tool_id: "doc_generator"
        description: "Create documentation files"
        permissions: ["read", "write"]
        target_dirs: ["docs/"]
      - tool_id: "example_builder"
        description: "Create example scripts and notebooks"
        permissions: ["read", "write"]
        target_dirs: ["examples/"]
      - tool_id: "notebook_creator"
        description: "Generate Jupyter notebooks"
        permissions: ["read", "write"]
      - tool_id: "ux_reviewer"
        description: "Validate documentation clarity and completeness"
        permissions: ["read"]
    boundaries:
      - "MUST NOT modify source code logic"
      - "MUST NOT modify specs"
      - "MUST sync docs with actual API behavior"
    success_criteria:
      - "README complete and accurate"
      - "At least one working pipeline example"
      - "All public APIs documented"

  R7:
    name: "RPM (Research Product Manager)"
    status: "active"
    responsibilities:
      - "Maintain TRACEABILITY.csv"
      - "Curate LITERATURE.bib"
      - "Write REPRODUCIBILITY.md"
      - "Manage preregistration artifacts"
    tools:
      - tool_id: "traceability_linker"
        description: "Update TRACEABILITY.csv with mappings"
        permissions: ["read", "write"]
        target_files: ["TRACEABILITY.csv"]
      - tool_id: "bibtex_builder"
        description: "Generate and validate BibTeX entries"
        permissions: ["read", "write"]
        target_files: ["LITERATURE.bib"]
      - tool_id: "reproducibility_checker"
        description: "Validate reproducibility instructions"
        permissions: ["read", "execute"]
      - tool_id: "preregistration_filler"
        description: "Generate preregistration.json from proposal"
        permissions: ["read", "write"]
        target_files: ["preregistration.json"]
    boundaries:
      - "MUST NOT modify source code"
      - "MUST NOT modify specs"
      - "MUST sync traceability after each phase"
    success_criteria:
      - "TRACEABILITY.csv complete for all Objectives"
      - "All DOIs in LITERATURE.bib"
      - "REPRODUCIBILITY.md tested and accurate"

communication:
  handoff_protocol:
    description: "How agents request work from each other"
    steps:
      - "Requesting agent logs request in DECISIONS.md"
      - "R1 validates request is within requester's boundaries"
      - "Target agent receives task with context"
      - "Target agent logs completion in DECISIONS.md"
  
  escalation_protocol:
    description: "How agents escalate blockers"
    steps:
      - "Agent logs blocker in DECISIONS.md with category"
      - "R1 assigns blocker to appropriate role"
      - "Resolution logged with decision rationale"

  review_protocol:
    description: "How agents review each other's work"
    steps:
      - "Producer marks artifact ready for review"
      - "Reviewer validates against success criteria"
      - "Issues logged; producer addresses them"
      - "Reviewer approves or requests another round"
```

### 6.3 Determining team composition

Not every project needs all seven roles. The Orchestrator (R1) determines team composition based on proposal characteristics:

**Minimal team (R1, R2, R4, R5):**
Use when:
- Proposal is purely technical (no novel research)
- Domain is well-understood by the implementer
- Documentation can be minimal
- No preregistration needed

**Standard team (R1, R2, R3, R4, R5, R6):**
Use when:
- Proposal involves domain-specific logic
- User-facing documentation is important
- Interactive pipeline needs good UX

**Full team (R1, R2, R3, R4, R5, R6, R7):**
Use when:
- `Novelty flag = true`
- Research reproducibility is critical
- Traceability to literature is required
- Preregistration needed

The decision MUST be recorded in `DECISIONS.md` with justification.

### 6.4 Tool manifest requirements

Each tool in an agent's manifest MUST specify:

- `tool_id`: Unique identifier within the agent's scope
- `description`: What the tool does
- `permissions`: Array of `["read", "write", "execute"]` as applicable
- `target_files` or `target_dirs` (optional): Explicit paths the tool can affect

Tools not in an agent's manifest are **forbidden** for that agent. If an agent needs a capability it lacks, it MUST request it through R1, who may either:
1. Add the tool to the manifest (logging in DECISIONS.md), or
2. Delegate the work to an agent who has the tool

### 6.5 Output of Phase 1A

At the end of Phase 1A, R1 MUST have produced:

1. `agents.yaml` – Complete configuration per Section 6.2
2. Entry in `DECISIONS.md` documenting:
   - Team composition rationale
   - Any roles excluded and why
   - Any custom tool additions

Only after `agents.yaml` exists may R1 authorize Phase 1B.

---

## 7. Task Specification for AI Agents

All work after specs is decomposed into **tasks** that AI agents can execute.

### 7.1 Task Spec format

Each task MUST be represented in a machine-readable format, e.g. YAML or JSON. Minimal fields:

- `task_id`: unique identifier (e.g. `A2.FN.001`, `PIPELINE.CLI.001`),
- `title`: short human-readable title,
- `assigned_to`: role ID (must match an active agent in `agents.yaml`),
- `inputs`: list of artefacts required (e.g. `["specs/A2.md", "proposal.normalized.json"]`),
- `constraints`: text describing assumptions or boundaries,
- `expected_tests`: list of test IDs that must pass when the task is complete,
- `required_tools`: list of tool_ids the agent will need (must be in their manifest),
- `coder_count`: number of coding agents,
- `reviewer_count`: number of reviewers/testers,
- `max_rounds`: maximum review/fix cycles,
- `validation_hook`: script or command that validates completion (e.g. `pytest -k test_pipeline_cli`).

The **task graph** must be acyclic and aligned with A2–A4.

### 7.2 Mandatory tasks

Every project MUST define tasks for:

- **Agent establishment** (`agents.yaml` creation) – assigned to R1

- **Spec authoring** (`A1`, `A2`, `A3`, `A4`, `A5`) – assigned to R2/R3

- **Python package setup** – assigned to R2/R4
  - Create `pyproject.toml` with metadata from proposal
  - Set up package structure (`src/` or flat layout)
  - Create `__init__.py` with `__version__` and `__all__`
  - Add `py.typed` marker if using type hints
  - Configure build backend

- **Dependency management** – assigned to R2/R4
  - Specify core dependencies in `pyproject.toml`
  - Define optional dependency groups (dev, test, docs)
  - Use `uv add` / `uv add --dev` for dependency changes
  - Maintain `uv.lock` with `uv lock`
  - Create `requirements*.txt` exports only if downstream tooling needs them
  - Document dependency rationale in A3

- **Code quality setup** – assigned to R4/R5
  - Configure ruff (or flake8/pylint) in `pyproject.toml`
  - Configure formatter (ruff format or black)
  - Configure mypy for type checking
  - Set up pre-commit hooks in `.pre-commit-config.yaml`

- **Core features implementation** (at least one task per public API feature) – assigned to R4
  - Implement functions/classes with type hints
  - Add docstrings in chosen format (Google/NumPy/Sphinx)
  - Follow PEP 8 naming and style conventions
  - Export in `__init__.py` if part of public API
  - Reuse existing library components where available; document any required custom implementations
  - Eliminate duplicate/redundant logic before task completion

- **Tests** – assigned to R4/R5
  - Unit tests (pytest) for each function/class
  - Integration tests for features
  - Acceptance tests for Objectives
  - Configure pytest in `pyproject.toml`
  - Set up fixtures in `conftest.py`
  - Achieve coverage thresholds from A5

- **Observability & persisted logging** – assigned to R4/R5
  - Implement centralized logging configuration and logger factory
  - Persist run-level structured logs to disk (`logs/` by default)
  - Persist statistics summaries to disk with schema defined in proposal
  - Add redaction/PII filtering hooks and retention policy controls
  - Add tests that fail if required log fields or files are missing

- **Interactive pipeline** (Section 10) – assigned to R4/R6
  - Implement CLI using click or argparse
  - Create notebook examples
  - Add web/TUI interface if specified
  - Test pipeline with CliRunner or nbmake

- **Documentation** – assigned to R6
  - Set up Sphinx with appropriate theme
  - Configure autodoc for API documentation
  - Write user guide and tutorials
  - Create examples in `examples/` directory
  - Add README with badges and quick start
  - Configure ReadTheDocs or GitHub Pages

- **Publication artifact plotting** – assigned to R6/R4
  - Generate `manuscript/artifact_manifest.yaml` from manuscript requirements
  - Implement publication-grade plot generators (vector + raster, style-controlled)
  - Validate mechanism completeness (manifest coverage + callable generators + entrypoint)
  - Run artifact rendering only in reproduction/integration runs (or fixture-data smoke mode)

- **CI/CD setup** – assigned to R4/R5
  - Create GitHub Actions workflow (or equivalent)
  - Set up matrix testing (Python versions, OS)
  - Configure coverage reporting (codecov/coveralls)
  - Add build and distribution checks
  - Set up automated PyPI publishing (optional)

- **Performance & scalability** – assigned to R4/R5
  - Define benchmark scenarios from expected dataset sizes and workflow complexity
  - Add benchmark tests for critical methods and pipeline stages
  - Profile hot paths and record optimization decisions in `DECISIONS.md`
  - Add guardrails for memory/runtime regressions in CI

- **Type checking** – assigned to R4
  - Add type hints to all public functions
  - Run mypy and fix type errors
  - Ensure `py.typed` is included in distribution
  - Add mypy to CI pipeline

- **Governance artefacts** – assigned to R7
  - `TRACEABILITY.csv` with agent attribution
  - `DECISIONS.md` with Python-specific decisions
  - `LITERATURE.bib` for citations
  - `REPRODUCIBILITY.md` with `uv` environment setup instructions
  - `preregistration.json` if Novelty flag = true

- **Build and distribution** – assigned to R4/R7
  - Test building with `uv build`
  - Verify wheel and sdist contents
  - Test installation in a clean `uv` virtual environment
  - Validate PyPI metadata and long description
  - Test install from built distributions (prefer `uv pip install`; verify plain `pip` compatibility if needed)

---

## 8. Implementation Phases (AI State Machine)

The AI Orchestrator (R1) follows this **state machine**:

### 8.1 PHASE 0 – READ_PROPOSAL

- Read `proposal.normalized.json`.
- Validate against DoR (Section 5).
- If invalid:
  - Generate a structured error report listing:
    - Missing fields,
    - Invalid URLs/DOIs,
    - Placeholder strings.
  - STOP and request proposal revision.

**Exit criteria:** DoR passes. Proposal is standardised.

### 8.2 PHASE 1A – ESTABLISH_AGENTS

This phase creates the foundation for all subsequent work by instantiating the agent team.

**R1 (Orchestrator) MUST:**

1. **Analyze proposal complexity**
   - Review `proposal.normalized.json` for:
     - Number of Objectives
     - Novelty flag value
     - Dataset complexity
     - Risk count and severity
   - Determine required team composition (Section 6.3)

2. **Instantiate agents**
   - For each active role, define:
     - Responsibilities specific to this project
     - Tool manifest with permissions
     - Boundaries (what the agent MUST NOT do)
     - Success criteria

3. **Define communication protocols**
   - How agents will hand off work
   - How escalations will be handled
   - How reviews will be conducted

4. **Produce `agents.yaml`**
   - Complete configuration per Section 6.2
   - Validate all required fields present
   - Ensure tool manifests are sufficient for planned work

5. **Log establishment decision**
   - Record in `DECISIONS.md`:
     - Team composition
     - Rationale for included/excluded roles
     - Any non-standard tool assignments

**Exit criteria:**
- `agents.yaml` exists and is valid
- All active agents have complete tool manifests
- `DECISIONS.md` contains establishment entry
- R1 has validated that tools cover all planned work

### 8.3 PHASE 1B – GENERATE_SPECS

- Agents R2 and R3 produce `specs/A1.md`–`specs/A5.md` based on the proposal.
- Each agent uses ONLY tools from their manifest in `agents.yaml`.
- Ensure each Objective is mapped to:
  - One or more features in A2,
  - One or more tests in A4.
- Ensure Interactive Pipeline has:
  - At least one feature entry in A2,
  - Corresponding architecture notes in A3,
  - Tests in A4.

**Exit criteria:**
- A1–A5 complete with no TBDs in core sections
- All Objectives mapped to features and tests
- Interactive pipeline documented in A2/A3/A4

### 8.4 PHASE 2 – BUILD_TASK_GRAPH

- Decompose A2/A3 into tasks (Section 7).
- Save as `tasks.yaml` (or similar).
- Each task MUST specify `assigned_to` matching an active agent.
- Each task MUST specify `required_tools` that exist in the assignee's manifest.
- Ensure:
  - Every public API feature has at least one implementation task.
  - Interactive pipeline has separate tasks for:
    - Core pipeline logic,
    - CLI/notebook/web wrapper,
    - End-to-end tests.

**Exit criteria:**
- `tasks.yaml` exists with all required tasks
- Task graph is acyclic
- All tasks assigned to agents with necessary tools

### 8.5 PHASE 3 – IMPLEMENT

- For each task in `tasks.yaml`:
  - R4 (Implementer) writes code and tests using only their authorized tools.
  - R5 (Tester) runs `validation_hook` and associated tests.
- No task is "done" until:
  - All `expected_tests` pass,
  - Coverage thresholds from A5 are met (where applicable).

**Exit criteria:**
- All implementation tasks complete
- All tests pass
- Coverage thresholds met

### 8.6 PHASE 4 – INTEGRATE_PIPELINE

- Implement and connect the interactive pipeline to the core API.
- Add end-to-end tests for the pipeline using small fixture data.
- Ensure:
  - Pipeline is accessible via at least one entrypoint (CLI, notebook, or web/TUI).
  - Pipeline behaviour and options are documented (A2, docs, examples).
- R6 (Documenter) creates at least one working example.

**Exit criteria:**
- Pipeline implemented and accessible
- End-to-end tests pass
- At least one example exists in `examples/`

### 8.7 PHASE 5 – GOVERN & DOCUMENT

- R7 fills in:
  - `TRACEABILITY.csv`,
  - `LITERATURE.bib`,
  - `REPRODUCIBILITY.md`.
- R6 completes:
  - User documentation,
  - README,
  - Additional examples if needed.
- R1 maintains `DECISIONS.md` throughout.
- Ensure these artefacts are consistent with:
  - Specs,
  - Code,
  - Tests.

**Exit criteria:**
- All governance artifacts complete
- Documentation matches implementation
- TRACEABILITY.csv covers all Objectives

### 8.8 PHASE 6 – VERIFY & RELEASE

- Run full test suite and CI checks (Section 11).
- Verify that acceptance criteria for all Objectives are satisfied.
- R1 conducts final review of:
  - Agent boundary compliance (no violations logged)
  - Artifact completeness
  - Traceability integrity
- Tag a release version (e.g. `research-grade-v1.0.0`) and record it in `DECISIONS.md`.

**Exit criteria:**
- All tests pass
- All Objectives accepted
- Release tagged and logged

The AI MUST NOT skip phases; it can iterate within a phase but must pass its exit criteria before moving to the next.

---

## 9. Traceability & Governance

### 9.1 TRACEABILITY.csv

Each row SHOULD link:

- Objective ID,
- Requirement ID (from A2/A4),
- Implementation path (code file + symbol),
- Test ID(s),
- Source DOI(s),
- Agent ID (who produced the implementation).

This allows any result to be traced back to its theoretical or empirical justification AND the agent who created it.

### 9.2 DECISIONS.md

A chronological log of key decisions, with:

- Date,
- Role (R1–R7),
- Phase,
- Decision,
- Alternatives considered,
- Justification.

Special entries that MUST appear:
- Phase 1A: Team establishment decision
- Any tool manifest modifications
- Any boundary violations (even if resolved)
- Phase transitions

### 9.3 LITERATURE.bib

BibTeX entries for:

- All DOIs in the proposal,
- Any new references added during implementation.

---

## 10. Mandatory Interactive Pipeline

Every package built under this blueprint MUST include at least one **interactive pipeline workflow**.

### 10.1 Interactive pipeline requirements

The interactive pipeline MUST:

1. **Be a first-class feature**
   - Represented in A2 with its own feature ID(s) (e.g. `PIPELINE.CLI.001`).
   - Have corresponding Objectives and acceptance tests in A4.

2. **Guide the user step-by-step**
   - From:
     - Data loading / selection,
     - Configuration of analysis/model,
     - Running the computation,
     - Inspecting and exporting results,
   - To meaningful outputs (plots, tables, metrics, files).

3. **Be integrable in automation**
   - Implemented as callable functions (e.g. `run_pipeline(config)`).
   - Used within at least one script or notebook in `examples/`.

4. **Be testable**
   - A4 must define at least one **end-to-end test** that:
     - Uses a small fixture dataset,
     - Runs the pipeline,
     - Asserts on key outputs (e.g. metrics, produced files, expected values).

5. **Support Manuscript Generation**
   - The pipeline MUST support a "reproduction mode" (e.g., `mytool.generate_artifacts()`) that:
     - Runs the full analysis on the provided dataset.
     - Saves all `manuscript_requirements` (Tables and Figures) to `manuscript/artifacts/`.
     - Ensures these outputs are publication-ready (high DPI, proper formatting).
   - Validation focus at build time is mechanism completeness (manifest + generators + entrypoint); full artifact rendering is verified in integration runs when data is available.
   - The package MUST include `manuscript/artifact_manifest.yaml` that maps each required table/figure to:
     - generator function,
     - source inputs,
     - output paths,
     - validation checks.

6. **Persist run and statistics logs**
   - The pipeline MUST emit structured run logs for each major stage.
   - The pipeline MUST persist statistical summaries (metrics and uncertainty outputs) to disk.
   - Log outputs MUST include `run_id` so analysis outputs and logs can be correlated.

### 10.2 Acceptable forms of pipeline

**PRIMARY: Pythonic Interactive Console** (REQUIRED for non-coder packages)

The preferred pattern is an **interactive console experience**, where users work in a Python/IPython console with a simple, user-friendly API:

- **Pattern 1: IPython/Python Console (RECOMMENDED)**

  Users interact via Python or IPython terminal with simple commands:

  ```python
  # Launch IPython
  $ ipython

  # Simple workflow
  In [1]: import mytool as mt

  In [2]: data = mt.read("samples.csv")
  Loaded 150 samples with 8 features

  In [3]: model = mt.pls(data, target="concentration")
  Building PLS model with auto-detected parameters...
  ✓ Model ready (R²=0.92, Q²=0.89)

  In [4]: model.plot("scores")  # Interactive plot window

  In [5]: model.summary()
  # Rich formatted output table

  In [6]: new_predictions = model.predict("unknowns.csv")

  In [7]: new_predictions.save("results.csv")
  ```

  **Requirements**:
  - Package provides simple, top-level functions (not buried in modules)
  - All common operations accessible through intuitive function names
  - Rich display integration (`_repr_html_`, `__repr__`, `__str__`)
  - IPython tab completion works for all methods
  - Matplotlib/plotly integration for interactive plots
  - Progress indicators for long operations

- **Pattern 2: Interactive Script Mode**

  For users who prefer scripts, provide template scripts with clear sections to modify:

  ```python
  # analysis_template.py - Modify marked sections and run
  import mytool as mt

  # ========== MODIFY THIS SECTION ==========
  data_file = "your_data.csv"
  target_column = "Y"
  n_components = "auto"  # or specify number
  # =========================================

  # Run analysis (no modification needed below)
  data = mt.read(data_file)
  model = mt.pls(data, target=target_column, n_components=n_components)
  model.summary()
  model.plot()
  predictions = model.predict()
  predictions.save("predictions.csv")
  print("✓ Analysis complete! Results saved to predictions.csv")
  ```

  Users run: `python analysis_template.py`

**SECONDARY: Command-Line Wizard** (Alternative for simple workflows)

- **CLI wizard (Click or Argparse)**
  - **Using Click (recommended)**:
    - Define commands with `@click.command()` decorators
    - Use `click.prompt()` for interactive questions
    - Use `click.option()` for command-line flags
    - Expose via entry point in `pyproject.toml`:
      ```toml
      [project.scripts]
      mytool-pipeline = "mytool.cli:main"
      ```
    - Example structure:
      ```python
      import click

      @click.command()
      @click.option('--method', type=click.Choice(['pls', 'pca']),
                    prompt='Analysis method')
      def pipeline(method: str):
          """Interactive analysis pipeline."""
          # Use click.prompt() for additional questions
          # Call core functions from mytool package
      ```

  - **Using Argparse (standard library)**:
    - Create parser with `argparse.ArgumentParser()`
    - Use `input()` for interactive prompts
    - Less elegant but no dependencies

  - **Testing**: Use `click.testing.CliRunner` or subprocess
    ```python
    from click.testing import CliRunner

    def test_pipeline():
        runner = CliRunner()
        result = runner.invoke(pipeline, input='pls\n')
        assert result.exit_code == 0
    ```

- **Jupyter Notebook pipeline**
  - Notebook in `examples/` or `notebooks/` directory
  - Clear sections with markdown headers:
    1. Setup and imports
    2. Configuration (editable parameters in code cells)
    3. Data loading
    4. Analysis execution
    5. Results visualization and export
  - **Requirements**:
    - Imports the package: `import mytool`
    - Uses public API, not implementation details
    - Includes narrative explanations in markdown cells
    - Can be executed top-to-bottom without errors
  - **Testing**:
    - Use `nbmake` pytest plugin: `pytest --nbmake notebooks/pipeline.ipynb`
    - Or `papermill` for parameterized execution
  - **Programmatic backend**:
    - Notebook should call functions from package
    - Core logic NOT duplicated in notebook
    - Example:
      ```python
      # In notebook
      from mytool import run_analysis
      results = run_analysis(data, method='pls')
      ```

**OPTIONAL: Notebook-Based Analysis** (For documentation/teaching)

- **Jupyter Notebook pipeline** (for reproducibility and sharing)
  - Notebook in `examples/` directory with step-by-step workflow
  - Each cell clearly documented
  - Can be exported to Python script
  - Good for tutorials, not primary interface

- **Configuration-driven pipeline**
  - Read from config file (YAML, TOML, JSON)
  - CLI command: `mytool run --config pipeline.yaml`
  - Example config:
    ```yaml
    # pipeline.yaml
    data:
      path: data.csv
    analysis:
      method: pls
      components: 5
    output:
      path: results/
    ```
  - Load with `pydantic` models for validation:
    ```python
    from pydantic import BaseModel

    class PipelineConfig(BaseModel):
        data: DataConfig
        analysis: AnalysisConfig
        output: OutputConfig
    ```

The blueprint does not prescribe which form to use; A2/A3 must document the choice and justify it based on user needs.

---

## 11. Reproducibility & CI

### 11.1 Reproducibility

`REPRODUCIBILITY.md` MUST describe:

- **Python environment setup**
  - Python version (exact or minimum)
    ```bash
    # Install and pin Python with uv
    uv python install 3.11
    uv python pin 3.11
    ```

  - Virtual environment creation
    ```bash
    # Create and use project venv
    uv venv
    ```

  - Package installation
    ```bash
    # Development environment from lock
    uv sync --all-extras
    ```

- **Dependency locking**
  - Lock file generation command
    ```bash
    # Generate/update lock file
    uv lock
    ```
  - Lock file location (`uv.lock`)
  - Instructions to regenerate lock file if needed

- **System dependencies** (if any)
  - OS-level packages (e.g., `graphviz`, `libhdf5-dev`)
  - Installation commands for common platforms:
    ```bash
    # Ubuntu/Debian
    sudo apt-get install <packages>

    # macOS (Homebrew)
    brew install <packages>

    # Windows (conda or manual)
    conda install -c conda-forge <packages>
    ```

- **Data acquisition**
  - URLs or DOIs for public datasets (from proposal)
  - Download scripts or instructions
  - Expected file paths and checksums
  - Synthetic data generation commands if datasets are simulated
  - Example:
    ```bash
    # Download data
    python scripts/download_data.py

    # Or generate synthetic data
    python scripts/generate_fixtures.py --seed 42
    ```

- **Seed handling for stochastic components**
  - Global seed setting approach
    ```python
    import random
    import numpy as np

    def set_seed(seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        # Add torch, tf seeds if applicable
    ```
  - Where seeds are set (tests, examples, pipelines)
  - Default seed values used in paper/results

- **Reproduction steps**
  - Complete workflow to regenerate all results
    ```bash
    # 1. Set up environment
    uv python pin 3.11
    uv venv
    uv sync --group dev --group test

    # 2. Download/generate data
    uv run python scripts/download_data.py

    # 3. Run analysis
    uv run python examples/main_analysis.py --seed 42

    # 4. Generate figures
    uv run python scripts/generate_figures.py

    # 5. Run tests to verify
    uv run pytest tests/ -v
    ```

  - Expected outputs (figures, tables, metrics, run logs, statistics logs)
  - Location of output files
  - Log output locations (for example `logs/runs/` and `logs/stats/`)
  - Validation commands to verify correctness

- **Docker/container support** (optional but recommended)
  - Dockerfile for complete environment
    ```dockerfile
    FROM python:3.11-slim
    WORKDIR /app
    RUN pip install uv
    COPY . .
    RUN uv sync --group dev --group test
    CMD ["uv", "run", "pytest"]
    ```
  - Build and run commands
  - Ensures cross-platform reproducibility

- **Troubleshooting common issues**
  - Platform-specific notes (Windows path issues, macOS permissions, etc.)
  - Known dependency conflicts and solutions
  - Performance considerations (memory, CPU usage)

### 11.2 Continuous Integration

CI MUST, at minimum:

- **Trigger on**:
  - Every push to main/develop branches
  - Every pull request
  - Scheduled runs (e.g., weekly) to catch dependency issues

- **Python version matrix**
  - Test on all supported Python versions (from `requires-python`)
  - Example: Python 3.9, 3.10, 3.11, 3.12

- **Operating system matrix** (if applicable)
  - Ubuntu (Linux) - primary
  - macOS - if targeting Mac users
  - Windows - if targeting Windows users

- **CI workflow steps** (example using GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Set up uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --group dev --group test

      - name: Lint with ruff
        run: uv run ruff check .

      - name: Format check with ruff
        run: uv run ruff format --check .

      - name: Type check with mypy
        run: uv run mypy src/<package>

      - name: Logging compliance tests
        run: uv run pytest tests/ -k logging -v

  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Set up uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --group test

      - name: Run tests with coverage
        run: |
          uv run pytest tests/ \
            --cov=<package> \
            --cov-report=xml \
            --cov-report=term \
            -v

      - name: Upload coverage to Codecov
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Set up uv
        uses: astral-sh/setup-uv@v4

      - name: Build package
        run: uv build

      - name: Check package metadata
        run: uvx twine check dist/*

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: distributions
          path: dist/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Set up uv
        uses: astral-sh/setup-uv@v4

      - name: Run pip-audit
        run: uvx pip-audit

      - name: Check for known vulnerabilities
        run: uvx safety check
```

- **Required checks that must pass**:
  1. **Linting**: `ruff check .` (or flake8/pylint) with zero errors
  2. **Formatting**: `ruff format --check .` ensures consistent style
  3. **Type checking**: `mypy src/<package>` passes with configured strictness
  4. **Unit tests**: All unit tests pass
  5. **Integration tests**: All integration tests pass
  6. **Acceptance tests**: All Objective-mapped tests pass
  7. **Coverage**: Meets minimum threshold (e.g., 80%+)
  8. **Logging compliance**: required run/statistics logs are persisted with required schema fields
  9. **Build**: `uv build` succeeds
  10. **Package validation**: `uvx twine check dist/*` passes
  11. **Security**: No known vulnerabilities in dependencies

- **Interactive pipeline tests**
  - CLI tests in headless mode (using CliRunner)
  - Notebook tests with `nbmake` or `papermill`
  - Web/TUI tests in headless mode or skipped with markers

- **Failure handling**
  - Any CI check failure blocks merge to main
  - Failures must be fixed; cannot be ignored or overridden
  - Package is **not** in research-grade state while CI fails

- **Performance benchmarks** (optional)
  - Use `pytest-benchmark` for performance regression tests
  - Store baseline results and compare in CI
  - Fail if performance degrades beyond threshold

- **Documentation builds** (see Section 11.3)
  - Sphinx builds without errors or warnings
  - Doctests pass
  - Link checking succeeds

### 11.3 Python Documentation Requirements

All Python packages built under this blueprint MUST provide comprehensive documentation following Python community standards.

- **README.md**
  - **Badges** at the top (optional but recommended)
    ```markdown
    [![PyPI version](https://badge.fury.io/py/<package>.svg)](https://pypi.org/project/<package>/)
    [![Python versions](https://img.shields.io/pypi/pyversions/<package>.svg)](https://pypi.org/project/<package>/)
    [![CI](https://github.com/<user>/<repo>/workflows/CI/badge.svg)](https://github.com/<user>/<repo>/actions)
    [![Coverage](https://codecov.io/gh/<user>/<repo>/branch/main/graph/badge.svg)](https://codecov.io/gh/<user>/<repo>)
    [![License](https://img.shields.io/pypi/l/<package>.svg)](https://github.com/<user>/<repo>/blob/main/LICENSE)
    ```

  - **Sections** (minimum required):
    1. Brief description (1-2 sentences)
    2. Key features (bulleted list)
    3. Installation (`uv add <package>` or `pip install <package>`)
    4. Quick start example (5-10 lines of code)
    5. Documentation link
    6. License
    7. Contributing (link to CONTRIBUTING.md if present)

  - **Example structure**:
    ```markdown
    # MyPackage

    Brief description of what the package does.

    ## Features

    - Feature 1
    - Feature 2
    - Feature 3

    ## Installation

    ```bash
    uv add mypackage
    ```

    ## Quick Start

    ```python
    from mypackage import main_function

    result = main_function(data)
    print(result)
    ```

    ## Documentation

    Full documentation is available at [https://mypackage.readthedocs.io](https://mypackage.readthedocs.io)

    ## License

    This project is licensed under the MIT License - see LICENSE file for details.
    ```

- **Sphinx documentation** (`docs/` directory)

  - **Setup with Sphinx**
    ```bash
    # Install Sphinx
    uv add --dev sphinx sphinx-rtd-theme

    # Initialize (one-time)
    sphinx-quickstart docs

    # Build
    cd docs && make html
    ```

  - **Configuration** (`docs/conf.py`)
    ```python
    import os
    import sys
    sys.path.insert(0, os.path.abspath('../src'))

    project = 'MyPackage'
    author = 'Your Name'
    release = '1.0.0'  # Or read from package

    extensions = [
        'sphinx.ext.autodoc',      # Auto-generate docs from docstrings
        'sphinx.ext.napoleon',     # Support Google/NumPy docstrings
        'sphinx.ext.viewcode',     # Add source code links
        'sphinx.ext.intersphinx',  # Link to other project docs
        'sphinx.ext.doctest',      # Test code examples
        'sphinx.ext.todo',         # Support TODO items
        'sphinx_rtd_theme',        # ReadTheDocs theme
    ]

    html_theme = 'sphinx_rtd_theme'

    # Napoleon settings for Google/NumPy style
    napoleon_google_docstring = True
    napoleon_numpy_docstring = True

    # Intersphinx mapping (link to Python, NumPy, etc.)
    intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
        'numpy': ('https://numpy.org/doc/stable/', None),
        'pandas': ('https://pandas.pydata.org/docs/', None),
    }
    ```

  - **Documentation structure**
    ```
    docs/
    ├── conf.py              # Sphinx configuration
    ├── index.rst            # Main landing page
    ├── installation.rst     # Installation instructions
    ├── quickstart.rst       # Quick start guide
    ├── user_guide/          # User guide pages
    │   ├── index.rst
    │   └── ...
    ├── api/                 # API reference
    │   ├── index.rst
    │   └── modules.rst
    ├── examples/            # Example notebooks/scripts
    │   └── ...
    ├── changelog.rst        # Changelog (link to CHANGELOG.md)
    └── contributing.rst     # Contribution guide
    ```

  - **Autodoc usage** for API documentation
    ```rst
    .. automodule:: mypackage.core
       :members:
       :undoc-members:
       :show-inheritance:

    .. autofunction:: mypackage.process_data

    .. autoclass:: mypackage.Model
       :members:
       :special-members: __init__
    ```

- **Docstrings** (inline code documentation)

  - **Choose one style consistently**: Google, NumPy, or Sphinx (reST)

  - **Google style** (recommended for readability):
    ```python
    def process_data(data: pd.DataFrame, method: str = "pls") -> np.ndarray:
        """Process input data using the specified method.

        This function applies the chosen dimensionality reduction method
        to the input data and returns the transformed array.

        Args:
            data: Input DataFrame with features in columns. Must have
                at least 2 columns and no missing values.
            method: Algorithm to use. Options are:
                - "pls": Partial Least Squares
                - "pca": Principal Component Analysis

        Returns:
            Transformed data as a 2D numpy array with shape (n_samples, n_components).

        Raises:
            ValueError: If method is not recognized or data is invalid.
            TypeError: If data is not a pandas DataFrame.

        Examples:
            >>> import pandas as pd
            >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            >>> result = process_data(df, method="pls")
            >>> result.shape
            (3, 2)

        Note:
            This function requires scikit-learn to be installed.

        See Also:
            fit_model: Fit a model using processed data.
        """
        pass
    ```

  - **NumPy style** (common in scientific packages):
    ```python
    def process_data(data, method="pls"):
        """
        Process input data using the specified method.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame with features in columns.
        method : str, default="pls"
            Algorithm to use ("pls" or "pca").

        Returns
        -------
        np.ndarray
            Transformed data array.

        Raises
        ------
        ValueError
            If method is not recognized.

        Examples
        --------
        >>> result = process_data(df, method="pls")
        """
        pass
    ```

  - **All public functions/classes MUST have docstrings**
  - **Module-level docstrings** at top of each file
    ```python
    """
    Core processing module for MyPackage.

    This module provides the main data processing functions including
    transformation, normalization, and analysis capabilities.
    """
    ```

- **Examples and tutorials**

  - **Location**: `examples/` directory
  - **Formats**:
    - Python scripts (`.py`) with comments
    - Jupyter notebooks (`.ipynb`) with narrative
  - **Content**: Each example should:
    - Be self-contained and runnable
    - Include installation instructions at top
    - Explain what it demonstrates
    - Show expected output
    - Use realistic but small data

- **Changelog** (`CHANGELOG.md`)

  - Follow [Keep a Changelog](https://keepachangelog.com/) format
    ```markdown
    # Changelog

    All notable changes to this project will be documented in this file.

    The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
    and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

    ## [Unreleased]

    ### Added
    - New feature X

    ## [1.0.0] - 2024-01-15

    ### Added
    - Initial release
    - Feature A, B, C

    ### Fixed
    - Bug in function Y
    ```

- **Contributing guide** (`CONTRIBUTING.md`)

  - How to set up development environment
  - Code style requirements (PEP 8, type hints)
  - How to run tests
  - How to submit pull requests
  - Code of conduct (optional)

- **Deployment**

  - **ReadTheDocs** (recommended for open source)
    - Free hosting for public repos
    - Automatic builds on push
    - Versioned documentation
    - Configuration in `.readthedocs.yml`

  - **GitHub Pages** (alternative)
    - Build Sphinx docs in CI
    - Deploy to `gh-pages` branch
    - Access at `https://<user>.github.io/<repo>/`

- **Doctests**

  - Code examples in docstrings that can be tested
  - Run with: `pytest --doctest-modules src/`
  - Include in CI to ensure examples stay current

---

## 12. Final Acceptance Checklist

Before calling a project "Done under BLUEPRINT-Universal-1.1", the Orchestrator (R1) MUST verify:

### 12.1 Proposal and Planning

1. **`proposal.normalized.json`** is archived, standardised, and passes DoR (Section 5)
   - All required fields present, including `Python package specifics`
   - No placeholders (`TBD`, `???`, etc.)
   - All DOIs/URLs validated

2. **`agents.yaml`** documents the team with complete tool manifests
   - All active roles defined with responsibilities
   - Tool manifests complete for each agent
   - Communication protocols specified

3. **A1–A5 specifications** are present, complete, and free of placeholders
   - A1: Package identity, Python version, success criteria defined
   - A2: All features have type-hinted signatures and docstrings
   - A3: Package structure, dependencies, architecture documented
   - A4: Test plan with pytest configuration complete
   - A5: All quality tools configured (ruff, mypy, pytest, coverage)

4. **All Objectives mapped** to:
   - Features in A2
   - Tests in A4
   - Rows in `TRACEABILITY.csv`

### 12.2 Python Package Structure

5. **`pyproject.toml`** is complete and valid
   - `[project]` section with all required metadata
   - `[build-system]` specifies build backend
   - `[project.scripts]` defines console entry points
   - `[project.optional-dependencies]` defines dev/test/docs extras
   - `uv.lock` exists and matches declared dependencies
   - All tool configurations present (`[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`, etc.)

6. **Package structure** follows specification
   - `src/<package_name>/__init__.py` exists with `__version__` and `__all__`
   - `src/<package_name>/py.typed` present if package includes type hints
   - Module hierarchy matches A3 architecture
   - No `__pycache__` or `.pyc` files in source control

7. **Dependencies** are properly specified
   - Core dependencies in `pyproject.toml` with version constraints
   - Optional dependencies grouped logically
   - No unnecessary or unused dependencies
   - All dependencies justified in A3

### 12.3 Code Quality

8. **Source code** implements all A2 features
  - All public functions/classes from A2 implemented
  - Type hints present on all public APIs (PEP 484)
  - Docstrings in consistent format (Google/NumPy/Sphinx)
  - PEP 8 naming conventions followed
   - Existing library components are reused where applicable; unnecessary custom rewrites are absent
   - No duplicate or redundant code paths remain in production modules

9. **Code quality checks pass**
    - `ruff check .` (or configured linter) returns zero errors
    - `ruff format --check .` confirms consistent formatting
    - `mypy src/<package>` passes with configured strictness
    - No `# type: ignore` without specific error codes
    - Structured logging configuration is present and enabled for analysis/pipeline paths

### 12.4 Testing

10. **All tests pass**
    - Unit tests: `pytest tests/unit/` (if separated)
    - Integration tests: `pytest tests/integration/`
    - Acceptance tests: All Objective-mapped tests pass
    - Pipeline tests: Interactive pipeline end-to-end tests pass
    - Logging tests: required run/statistics log files and fields are validated

11. **Coverage thresholds met**
    - Line coverage ≥ threshold specified in A5 (e.g., 80%)
    - Coverage report generated: `pytest --cov=<package> --cov-report=html`
    - No critical code paths untested

12. **Test organization**
    - Tests mirror source structure
    - Fixtures in `conftest.py`
    - Test markers configured and used appropriately

### 12.5 Interactive Pipeline & User Experience

13. **Pythonic user-friendly interface** requirements met (if `non_coder_interface_required = true`):
    - **Simple top-level API** accessible via `import mytool as mt`
    - **Short, memorable function names** (`read()`, `plot()`, `summary()`)
    - **Method chaining** works for fluent workflows
    - **Rich terminal output** using `rich` or similar (formatted tables, progress bars)
    - **IPython integration** works (tab completion, rich display, help)
    - **Interactive plots** open in windows (matplotlib/plotly)
    - **Sensible defaults** for all parameters
    - **User-friendly error messages** with suggestions

14. **Object-Oriented design** validated:
    - **Core domain classes** defined (e.g., `Model`, `Dataset`, `Pipeline`)
    - **Class hierarchy** documented in A3
    - **Abstract base classes** used where appropriate
    - **Encapsulation** demonstrated (properties, private attributes with `_`)
    - **Composition** used appropriately
    - **Design patterns** documented (Factory, Strategy, Builder, etc.)

15. **Non-coder usability** tested:
    - **One-liner workflows** exist for common tasks
    - **Template scripts** provided with clear modification sections
    - **Example sessions** work as documented
    - **Error messages** tested for clarity (no technical jargon)
    - **Default behavior** works without configuration (80% use cases)

16. **Interactive pipeline** general requirements:
    - Pipeline documented in A2/A3 and A6
    - Pipeline example in `examples/` directory
    - End-to-end test passes
    - Terminal-based interface works in IPython/Python console
    - `manuscript/artifact_manifest.yaml` exists and covers all required artifacts
    - Artifact generation entrypoint is implemented and smoke-tested on fixture data when available
    - Full table/figure rendering is not required at package-validation time; it is required in analysis/reproduction runs

### 12.6 Documentation

17. **README.md** is complete
    - Badges present (PyPI, CI, coverage, license)
    - Installation instructions clear
    - Quick start example works
    - Link to full documentation

18. **Sphinx documentation** built successfully
    - `cd docs && make html` completes without errors
    - All public APIs documented via autodoc
    - Examples included in docs
    - Doctests pass: `pytest --doctest-modules src/`
    - **Non-coder friendly**: Includes "Getting Started" tutorial, troubleshooting FAQ, glossary

19. **CHANGELOG.md** is current
    - Follows Keep a Changelog format
    - Latest version documented
    - All significant changes listed

### 12.7 Build and Installation

20. **Package builds successfully**
    - `uv build` completes without errors
    - Both wheel (`.whl`) and sdist (`.tar.gz`) created in `dist/`
    - `uvx twine check dist/*` passes with no warnings

21. **Package installs in clean environment**
    ```bash
    uv venv test_venv
    test_venv\Scripts\python -m pip install dist/<package>-<version>-py3-none-any.whl  # Windows
    test_venv/bin/python -m pip install dist/<package>-<version>-py3-none-any.whl       # Linux/macOS
    test_venv\Scripts\python -c "import <package>; print(<package>.__version__)"         # Windows
    test_venv/bin/python -c "import <package>; print(<package>.__version__)"              # Linux/macOS
    # Test user-friendly interface
    uv run --python test_venv\Scripts\python ipython -c "import <package> as mt; help(mt)"  # Windows
    uv run --python test_venv/bin/python ipython -c "import <package> as mt; help(mt)"       # Linux/macOS
    ```
    - All commands succeed
    - Package imports correctly
    - Version string matches expected
    - User-friendly API works (simple import, intuitive functions)

22. **PyPI metadata valid**
    - Long description renders correctly (test on TestPyPI or check locally)
    - Classifiers appropriate
    - License identifier correct (SPDX format)
    - URLs (homepage, repository, documentation) are valid

### 12.8 Governance and Reproducibility

23. **Governance artefacts** complete and current:
    - `TRACEABILITY.csv`: All Objectives → Features → Code → Tests → Sources
    - `DECISIONS.md`: All major decisions logged with agent attribution
    - `LITERATURE.bib`: All DOIs/references in BibTeX format
    - `REPRODUCIBILITY.md`: Complete environment setup and reproduction steps

24. **`REPRODUCIBILITY.md` verified**
    - Instructions tested in fresh environment
    - All data acquisition steps work
    - All analysis scripts run successfully
    - Results match expected outputs
    - Log output and statistics log locations are documented and reproducible

25. **Preregistration** (if `Novelty flag = true`)
    - `preregistration.json` generated from proposal
    - Uploaded to appropriate registry (OSF, AsPredicted, etc.)
    - URL recorded in proposal and `DECISIONS.md`

### 12.9 CI/CD and Operations

26. **CI pipeline passes** on clean branch
    - All quality checks (lint, format, type) pass
    - All tests pass on all target Python versions and OS
    - Coverage uploaded and meets threshold
    - Logging compliance tests pass
    - Build and package validation succeed
    - Security scans pass (`uvx pip-audit`, `uvx safety check`)
    - Performance benchmark checks pass against agreed thresholds

27. **No agent boundary violations** remain unresolved
    - All agents operated within their tool manifests
    - Any violations documented and justified in `DECISIONS.md`

28. **Pre-commit hooks** configured (optional but recommended)
    - `.pre-commit-config.yaml` present
    - Hooks installed: `pre-commit install`
    - Hooks pass: `pre-commit run --all-files`

### 12.10 Release

29. **Version management**
    - Version number follows semantic versioning (MAJOR.MINOR.PATCH)
    - Version consistent across:
      - `pyproject.toml`
      - `src/<package>/_version.py` or `__init__.py`
      - Git tag
      - `CHANGELOG.md`

30. **Release tagged** and logged
    - Git tag created: `git tag -a v1.0.0 -m "Release version 1.0.0"`
    - Tag pushed: `git push origin v1.0.0`
    - Release logged in `DECISIONS.md` with:
      - Date
      - Version number
      - Agent(s) who performed release
      - Summary of changes

31. **Optional: PyPI publication** (if releasing publicly)
    - Test publication to TestPyPI successful
    - Production publication to PyPI successful
    - Package installable via published distribution (`uv add <package>` and/or `pip install <package>`)
    - Package page on PyPI displays correctly

---

Only when **ALL** items (1-31) are verified and checked may the package be considered **research-grade, Python-compliant, OO-designed, and non-coder accessible**.

---

## 13. Using This Blueprint with Claude Code

This section explains how to use this blueprint **specifically with Claude Code**, which has a different agent model than the abstract R1-R7 roles defined earlier.

### 13.1 Claude Code Agent Mapping

The blueprint's conceptual roles (R1-R7) map to Claude Code's actual capabilities as follows:

| Blueprint Role | Claude Code Implementation | How to Invoke |
|---------------|---------------------------|---------------|
| **R1 - Orchestrator** | You (human) + Claude in main conversation | Direct conversation with Claude |
| **R2 - Architect** | `Plan` agent or main Claude | Use `EnterPlanMode` or ask Claude to design architecture |
| **R3 - Domain Scientist** | `Explore` agent + main Claude | Use Task tool with `subagent_type='Explore'` for research |
| **R4 - Implementer** | Main Claude with Write/Edit tools | Claude writes code directly in conversation |
| **R5 - Tester** | Main Claude with Bash tool | Claude runs `pytest` via Bash |
| **R6 - Documenter** | Main Claude with Write tool | Claude writes docs directly |
| **R7 - RPM** | Main Claude with Write/Edit tools | Claude maintains governance files |

**Key insight**: Instead of 7 separate agents, you'll have **1-3 Claude instances** playing multiple roles.

### 13.2 Practical Workflow with Claude Code

Here's how to actually use this blueprint with Claude Code:

#### Step 1: Prepare Your Proposal

Create `proposal.normalized.json` following Section 2.1. **Tip**: Ask Claude to help you create this from an unstructured description:

```bash
$ claude

You: I have a project idea. Can you help me create a proposal.normalized.json
     following BLUEPRINT-Universal-1_1.md Section 2.1?

     My idea: [describe your project]

Claude: [Asks clarifying questions and generates proposal.normalized.json]
```

#### Step 2: Validate Proposal (Phase 0)

```bash
You: Read proposal.normalized.json and BLUEPRINT-Universal-1_1.md.
     Validate the proposal against the DoR in Section 5.

Claude: [Validates and reports any issues]
```

#### Step 3: Generate Specifications (Phases 1A-1B)

Since Claude Code doesn't use formal `agents.yaml`, skip the agent establishment and go straight to specs:

```bash
You: Acting as R2 (Architect) and R3 (Domain Scientist),
     generate A1-A6 specifications following Section 4.
     Start with A1, then we'll review and continue.

Claude: [Generates A1.md]

You: [Review, provide feedback]

You: Good! Now generate A2 with the Python type hints and OO design
     as specified in Section 4.2 and 4.6.

Claude: [Generates A2.md]

[Continue for A3-A6]
```

#### Step 4: Generate Package Structure (Phase 2)

```bash
You: Create the Python package structure following A3 architecture.
     Use the src/ layout and create pyproject.toml per Section 2.3.

Claude: [Creates directory structure, pyproject.toml, __init__.py, etc.]
```

#### Step 5: Implement Features (Phase 3)

You can work iteratively:

```bash
You: Implement the core Model class hierarchy from A2, following the
     OO design patterns in A6. Start with BaseModel abstract class.

Claude: [Implements BaseModel using ABC]

You: Now implement PLSModel as a concrete subclass.

Claude: [Implements PLSModel]

You: Add the user-friendly interface - the simple mt.pls() function
     that non-coders can use.

Claude: [Adds convenience function]
```

#### Step 6: Implement Tests (Phase 3 continued)

```bash
You: Create pytest tests for PLSModel following A4 test plan.

Claude: [Creates test_pls_model.py with fixtures]

You: Run the tests.

Claude: [Uses Bash tool to run pytest, shows results]
```

#### Step 7: Interactive Pipeline (Phase 4)

```bash
You: Implement the user-friendly interactive console interface from Section 10.
     It should work in IPython with simple commands.

Claude: [Implements user-friendly API with __repr__, summary(), plot(), etc.]

You: Create a template script that non-coders can modify and run.

Claude: [Creates analysis_template.py]
```

#### Step 8: Documentation (Phase 5)

```bash
You: Set up Sphinx documentation following Section 11.3.
     Include getting started tutorial for non-coders.

Claude: [Creates docs/ structure, conf.py, writes tutorials]
```

#### Step 9: CI/CD (Phase 5 continued)

```bash
You: Create GitHub Actions CI workflow following Section 11.2.

Claude: [Creates .github/workflows/ci.yml]
```

#### Step 10: Final Validation (Phase 6)

```bash
You: Go through the Final Acceptance Checklist in Section 12.
     Check items 1-31 and report status.

Claude: [Reviews all items, creates checklist with status]

You: Build the package and test installation.

Claude: [Runs uv build, tests in clean uv environment]
```

### 13.3 Using Claude Code Agents Effectively

**For large projects**, use agents to parallelize work:

```bash
# Spawn multiple agents in parallel
You: Launch 3 agents in parallel:
     1. Explore agent: Research similar Python packages and their OO designs
     2. Plan agent: Design the class hierarchy for our models
     3. General agent: Set up the initial package structure

Claude: [Launches 3 agents simultaneously]
```

**For exploration**, use the Explore agent:

```bash
You: Use the Explore agent to find examples of user-friendly Python interfaces
     in existing packages like pandas, seaborn, etc.

Claude: [Launches Explore agent to search codebase and web]
```

### 13.4 Simplifying the Blueprint for Claude Code

Since Claude Code doesn't use formal agent manifests, you can **simplify** Section 6 (agents.yaml):

**Instead of creating `agents.yaml`**, just keep a simple `ROLES.md`:

```markdown
# Project Roles

- **Architect (R2)**: Claude - designs specs
- **Implementer (R4)**: Claude - writes code
- **Tester (R5)**: Claude - runs tests
- **Documenter (R6)**: Claude - writes docs
- **Orchestrator (R1)**: You - guide the process
```

### 13.5 Recommended Claude Code Prompts

Save these as **slash commands** in `.claude/commands/`:

**`.claude/commands/validate-proposal.md`**:
```markdown
Read proposal.normalized.json and validate it against BLUEPRINT-Universal-1_1.md Section 5 DoR.
Report any missing fields or issues.
```

**`.claude/commands/generate-specs.md`**:
```markdown
Generate specification documents A1-A6 following BLUEPRINT-Universal-1_1.md Section 4.
Focus on Python OO design and non-coder accessibility (user-friendly interface).
Ask me questions if the proposal is ambiguous.
```

**`.claude/commands/check-ux.md`**:
```markdown
Review the package against Section 4.6 (UX & Non-Coder Accessibility).
Check:
- Is there a simple, user-friendly API?
- Are there sensible defaults?
- Do error messages help non-coders?
- Is the OO design clean and extensible?
```

**`.claude/commands/run-checklist.md`**:
```markdown
Go through Section 12 Final Acceptance Checklist (items 1-31).
For each item, check current status and report what's missing.
```

### 13.6 Handling Complex Multi-Agent Scenarios

For **very large packages**, you might actually want separate Claude sessions:

1. **Session 1 (Planning)**: Use Plan agent to create A1-A6
2. **Session 2 (Implementation)**: Implement core classes
3. **Session 3 (Testing)**: Create comprehensive test suite
4. **Session 4 (Documentation)**: Write user docs and examples

Then **merge** the work using git.

### 13.7 Key Differences from Abstract Blueprint

| Blueprint Concept | Claude Code Reality |
|------------------|---------------------|
| `agents.yaml` with tool manifests | Not needed - Claude has all tools |
| Strict phase gates | Flexible conversation flow |
| 7 distinct agent instances | 1-3 Claude instances with role-playing |
| Tool authorization checks | Claude uses all available tools |
| Phase state machine | Human guides phases conversationally |

### 13.8 Claude Code Skills for Autonomous Execution

To enable **autonomous execution** following this blueprint, create these custom skills in `.claude/skills/`:

#### Skill 1: `blueprint-validate-proposal.md`

```markdown
# Validate Proposal Against Blueprint

## Objective
Validate `proposal.normalized.json` against BLUEPRINT-Universal-1_1.md Section 5 Definition of Ready (DoR).

## Process
1. Read `proposal.normalized.json`
2. Read `BLUEPRINT-Universal-1_1.md` Section 5.2
3. Check all DoR criteria:
   - Schema validity (all required fields present)
   - No placeholders (TBD, ???, REPLACE-ME)
   - Data URLs reachable
   - Novelty flag + preregistration consistency
   - Python package specifics present
   - User experience fields present
4. Generate validation report

## Success Criteria
- All DoR checks pass OR
- Clear report of what needs fixing

## Output
Create `validation-report.md` with status of each DoR item.
```

#### Skill 2: `blueprint-generate-specs.md`

```markdown
# Generate A1-A6 Specifications

## Objective
Generate complete specification documents A1-A6 following BLUEPRINT-Universal-1_1.md Section 4, with emphasis on Python OO design and non-coder accessibility.

## Prerequisites
- `proposal.normalized.json` exists and passes DoR
- `BLUEPRINT-Universal-1_1.md` available

## Process
1. Read proposal to understand objectives, scope, data
2. Generate `specs/A1.md` - Project & Package Definition
   - Include Python version, PyPI metadata
   - Define success criteria
3. Generate `specs/A2.md` - Features & Public API
   - Define OO class hierarchy
   - Define user-friendly top-level functions
   - Include type hints and docstrings
4. Generate `specs/A3.md` - Architecture & Dependencies
   - Document OO design patterns
   - Define package structure (src/ layout)
   - List dependencies
5. Generate `specs/A4.md` - Data Handling & Test Plan
   - Define pytest configuration
   - Map tests to objectives
6. Generate `specs/A5.md` - Quality, CI, and Operations
   - Configure ruff, mypy, pytest
   - Define CI workflow
7. Generate `specs/A6.md` - UX & Non-Coder Accessibility
   - Define user-friendly interface requirements
   - Define OO class design
   - Define sensible defaults

## Success Criteria
- All 6 spec files created
- No TBD or placeholders in critical sections
- All objectives mapped to features
- OO design patterns documented
- User-friendly interface specified

## Autonomy Level
- Ask user for clarification ONLY if proposal is ambiguous
- Make reasonable design decisions based on best practices
- Document decisions in specs
```

#### Skill 3: `blueprint-setup-package.md`

```markdown
# Set Up Python Package Structure

## Objective
Create complete Python package structure following specs A1-A3.

## Prerequisites
- `specs/A1.md` through `specs/A6.md` exist

## Process
1. Create directory structure (src/ layout):
   ```
   project_root/
   ├── src/
   │   └── <package_name>/
   │       ├── __init__.py
   │       ├── _version.py
   │       ├── py.typed
   │       ├── core/
   │       ├── models/
   │       └── utils/
   ├── tests/
   ├── docs/
   ├── examples/
   └── ...
   ```

2. Create `pyproject.toml` from proposal Python package specifics:
   - [project] section with metadata
   - [build-system]
   - [project.scripts] for entry points
   - [project.optional-dependencies]
   - [tool.*] sections for ruff, mypy, pytest, coverage

3. Create `src/<package>/__init__.py`:
   - Import main classes and functions
   - Define __version__
   - Define __all__ for public API

4. Create configuration files:
   - `.python-version`
   - `.gitignore`
   - `README.md` skeleton
   - `LICENSE`

## Success Criteria
- Package structure matches A3
- pyproject.toml is PEP 621 compliant
- Can run `uv sync` successfully

## Autonomy Level
- Fully autonomous
- Use proposal data directly
```

#### Skill 4: `blueprint-implement-oo-core.md`

```markdown
# Implement Object-Oriented Core Classes

## Objective
Implement core domain classes following OO design patterns from specs A2 and A6.

## Prerequisites
- Package structure exists
- `specs/A2.md` and `specs/A6.md` define classes

## Process
1. Identify class hierarchy from A6
2. Implement abstract base classes first:
   ```python
   from abc import ABC, abstractmethod

   class BaseModel(ABC):
       @abstractmethod
       def fit(self, X, y):
           pass

       @abstractmethod
       def predict(self, X):
           pass
   ```

3. Implement concrete classes:
   - Follow encapsulation (use properties)
   - Add type hints on all methods
   - Add comprehensive docstrings
   - Implement __repr__ for nice display

4. For each class:
   - Create in appropriate module (src/<package>/models/, etc.)
   - Follow naming conventions from A2
   - Include all methods from A2 signatures

## Success Criteria
- All classes from A2 implemented
- Abstract base classes use ABC
- All public methods have type hints and docstrings
- Classes follow OO principles (encapsulation, inheritance, composition)

## Autonomy Level
- Fully autonomous for standard patterns
- Ask user for domain-specific algorithm details if needed
```

#### Skill 5: `blueprint-implement-python-interface.md`

```markdown
# Implement User-Friendly Python Interface

## Objective
Create a simple, user-friendly Python interface for non-coders following A6 specifications.

## Prerequisites
- Core OO classes implemented
- `specs/A6.md` defines user-friendly interface requirements

## Process
1. In `src/<package>/__init__.py`, create convenience functions:
   ```python
   def read(filepath: str) -> Dataset:
       """Load data from a file path."""
       return Dataset.from_file(filepath)

   def pls(data: Dataset, target: str, **kwargs) -> PLSModel:
       """Build and fit a PLS model."""
       model = PLSModel(**kwargs)
       model.fit(data, target)
       return model
   ```

2. Enhance classes with rich display:
   - `__repr__` for clean terminal output
   - `_repr_html_` for Jupyter
   - `summary()` method with formatted tables
   - `plot()` method for interactive plots

3. Add method chaining support:
   ```python
   class Pipeline:
       def load(self, path):
           self.data = Dataset.from_file(path)
           return self

       def scale(self):
           self.data = self.data.scaled()
           return self
   ```

4. Create template script in `examples/analysis_template.py`

## Success Criteria
- Top-level functions work: `import pkg as p; p.read()`, `p.pls()`
- Methods chain: `p.Pipeline().load().scale().fit()`
- Rich output in terminal and Jupyter
- Template script works for non-coders

## Autonomy Level
- Fully autonomous
- Follow A6 examples
```

#### Skill 6: `blueprint-implement-tests.md`

```markdown
# Implement Test Suite

## Objective
Create comprehensive pytest test suite following A4 test plan.

## Prerequisites
- Core classes implemented
- User-friendly interface implemented
- `specs/A4.md` defines test matrix

## Process
1. Create `tests/conftest.py` with fixtures:
   ```python
   @pytest.fixture
   def sample_data():
       return generate_test_data()
   ```

2. For each class/function, create test file:
   - `tests/test_<module>.py`
   - Mirror source structure
   - Use parametrize for multiple scenarios

3. Test categories:
   - Unit tests (test each method in isolation)
   - Integration tests (test workflows)
   - Acceptance tests (test objectives from proposal)
   - Interface tests (test convenience functions)

4. Configure pytest in `pyproject.toml`:
   - Set markers
   - Set coverage thresholds
   - Configure test discovery

5. Run tests and ensure they pass

## Success Criteria
- All expected tests from A4 implemented
- Tests pass: `pytest tests/ -v`
- Coverage ≥ threshold from A5
- Each objective has at least one acceptance test

## Autonomy Level
- Fully autonomous
- Generate realistic test data
```

#### Skill 7: `blueprint-setup-documentation.md`

```markdown
# Set Up Documentation

## Objective
Create Sphinx documentation with non-coder friendly content following Section 11.3.

## Prerequisites
- Code implemented
- User-friendly interface works

## Process
1. Initialize Sphinx in `docs/`:
   - Run sphinx-quickstart
   - Configure for autodoc
   - Set up ReadTheDocs theme

2. Create documentation structure:
   - `docs/index.rst` - landing page
   - `docs/installation.rst`
   - `docs/quickstart.rst` - user-friendly examples
   - `docs/user_guide/` - detailed guides
   - `docs/api/` - API reference
   - `docs/troubleshooting.rst`

3. Configure `docs/conf.py`:
   - Enable autodoc, napoleon
   - Set up intersphinx
   - Configure theme

4. Write non-coder friendly content:
   - Getting started tutorial (copy-paste examples)
   - Troubleshooting FAQ
   - Glossary of terms
   - Screenshot-based guides if possible

5. Build docs: `cd docs && make html`

## Success Criteria
- Docs build without errors
- API reference auto-generated
- Getting started tutorial works
- Doctests pass

## Autonomy Level
- Fully autonomous
- Generate examples from A6
```

#### Skill 8: `blueprint-setup-ci.md`

```markdown
# Set Up CI/CD Pipeline

## Objective
Create GitHub Actions CI/CD workflow following Section 11.2.

## Prerequisites
- Tests exist and pass
- Quality tools configured

## Process
1. Create `.github/workflows/ci.yml`
2. Configure matrix testing (Python versions, OS)
3. Add jobs:
   - Linting (ruff check)
   - Formatting (ruff format --check)
   - Type checking (mypy)
   - Tests (pytest with coverage)
   - Build (uv build)
   - Security (uvx pip-audit)

4. Configure coverage upload (codecov)

5. Test CI locally if possible

## Success Criteria
- CI workflow file exists
- All jobs defined
- Workflow is syntactically valid

## Autonomy Level
- Fully autonomous
- Use template from Section 11.2
```

#### Skill 9: `blueprint-final-validation.md`

```markdown
# Run Final Validation Checklist

## Objective
Validate package against all 31 items in Section 12 Final Acceptance Checklist.

## Prerequisites
- Package fully implemented
- Tests passing
- Docs built
- CI configured

## Process
1. Go through each item in Section 12:
   - Items 1-4: Proposal and Planning
   - Items 5-7: Package Structure
   - Items 8-9: Code Quality
   - Items 10-12: Testing
   - Items 13-16: Interactive Pipeline & UX
   - Items 17-19: Documentation
   - Items 20-22: Build and Installation
   - Items 23-25: Governance
   - Items 26-28: CI/CD
   - Items 29-31: Release

2. For each item:
   - Check if it's complete
   - Run validation commands
   - Document status

3. Create `VALIDATION_REPORT.md` with:
   - Checklist with checkmarks
   - Items that need attention
   - Recommended next steps

4. Test package installation in clean venv

## Success Criteria
- All 31 items validated
- Clear report of any gaps
- Package installable and functional

## Autonomy Level
- Fully autonomous
- Report findings to user
```

#### Skill 10: `blueprint-orchestrator.md` (Master Skill)

```markdown
# Blueprint Orchestrator - Autonomous Package Builder

## Objective
Autonomously build a complete Python package following BLUEPRINT-Universal-1_1.md from proposal to release.

## Prerequisites
- `proposal.normalized.json` exists
- `BLUEPRINT-Universal-1_1.md` available

## Process
Execute sub-skills in order:

1. **Validate** (`blueprint-validate-proposal`)
   - If fails: Report issues and stop

2. **Generate Specs** (`blueprint-generate-specs`)
   - Creates A1-A6
   - Ask user to review A1-A6 before proceeding

3. **Setup Package** (`blueprint-setup-package`)
   - Creates structure and pyproject.toml

4. **Implement Core** (`blueprint-implement-oo-core`)
   - Builds OO class hierarchy

5. **Implement User-Friendly Interface** (`blueprint-implement-python-interface`)
   - Creates non-coder friendly API

6. **Implement Tests** (`blueprint-implement-tests`)
   - Full test suite

7. **Publication Artifacts** (`blueprint-plot-publication-artifacts`)
   - Generate publication-grade tables and figures

8. **Setup Docs** (`blueprint-setup-documentation`)
   - Sphinx documentation

9. **Setup CI** (`blueprint-setup-ci`)
   - GitHub Actions workflow

10. **Final Validation** (`blueprint-final-validation`)
   - 31-point checklist

11. **Report** to user with status and next steps

## User Interaction Points
- After specs (Step 2): Review A1-A6
- After validation (Step 10): Review final report

## Success Criteria
- Package passes all 31 validation items
- Package is installable and functional
- All objectives from proposal achieved

## Autonomy Level
- Highly autonomous
- Minimal user intervention (2 review points)
- Makes design decisions based on best practices
- Documents all decisions in specs and DECISIONS.md
```

### 13.9 How to Use Skills for Autonomous Execution

**Installation:**
1. Create `.claude/skills/` directory in your project
2. Save each skill as a markdown file (e.g., `blueprint-orchestrator.md`)
3. Claude Code will auto-detect them

**Usage:**

```bash
# Simple: Run orchestrator for full autonomous build
$ claude
You: Use the blueprint-orchestrator skill with my proposal.normalized.json

Claude: [Executes all steps autonomously, pausing only for A1-A6 review]

# Advanced: Run individual skills
You: Use blueprint-implement-python-interface skill

Claude: [Implements user-friendly interface autonomously]

# Parallel: Run multiple skills simultaneously
You: Run these skills in parallel:
     - blueprint-implement-oo-core
     - blueprint-setup-documentation
     - blueprint-setup-ci

Claude: [Launches 3 agents in parallel]
```

**Benefits:**
- ✅ Fully autonomous execution following blueprint
- ✅ Consistent quality (skills encode best practices)
- ✅ Parallel execution for faster builds
- ✅ Reusable across projects
- ✅ Easy to update/improve skills

### 13.10 Example: Complete Session

Here's a realistic complete session:

```bash
$ claude

You: I want to build a Python package for chemometric analysis.
     Let's follow BLUEPRINT-Universal-1_1.md.

     First, help me create proposal.normalized.json.

Claude: [Asks questions about objectives, data, etc.]

You: [Provides answers]

Claude: [Generates proposal.normalized.json]

You: Validate this against the DoR.

Claude: [Validates - finds missing preregistration URL]

You: Add placeholder for preregistration, we'll do that later.

Claude: [Updates proposal]

You: Generate A1-A6 specifications. Focus on OO design and
     making it usable for chemists who don't code much.

Claude: [Generates specs, asking clarifying questions]

You: [Reviews A1-A6, gives feedback]

You: Create the package structure with pyproject.toml.

Claude: [Creates structure]

You: Implement the core classes from A2.

Claude: [Implements classes]

You: Add the user-friendly interface so users can do:
     >>> import chemtool as ct
     >>> data = ct.read("spectra.csv")
     >>> model = ct.pls(data, target="concentration")
     >>> model.plot()

Claude: [Implements user-friendly API]

You: Create tests.

Claude: [Creates pytest tests]

You: Run tests.

Claude: pytest tests/ -v
[Shows test results]

You: Set up docs.

Claude: [Sets up Sphinx with getting-started guide]

You: Run the final checklist.

Claude: [Goes through Section 12, reports 28/31 items complete]

You: Fix the remaining items.

Claude: [Addresses gaps]

You: Build and test installation.

Claude: uv build
[Tests installation in clean uv environment]

You: Excellent! Create a git tag v1.0.0.

Claude: [Creates tag]
```

## 14. Quickstart: How to Use This with External AI Tools

This section gives you a **ready-made pattern** for using this blueprint with tools like non-Claude AI assistants, Copilot, or Code Interpreter.

### 14.1 Human preparation steps

You have **two options**:

1. **If you already have a standardised proposal:**
   - Create and fill `proposal.normalized.json` following Section 2.1.  
   - Check that it is **standardised** and passes the DoR in Section 5.  
   - Place `BLUEPRINT-Universal-1.1.md` and `proposal.normalized.json` together in a project folder (or otherwise make them both available to the AI).

2. **If you only have unstructured documents (e.g. Word/PDF):**
   - Put your raw proposal docs (e.g. `Goal.docx`, notes, outline) in the project folder.
   - Make sure `BLUEPRINT-Universal-1.1.md` is also present.
   - Instruct the AI to first run **Phase -1** (Section 5.3) using a three-expert panel to produce a standardised `proposal.normalized.json` that passes DoR.
   - After that, the AI can proceed with PHASES 0–6 (Section 8).

### 14.2 Example system / instruction prompt for an external AI

You can adapt this template to your AI tool:

> **System / Developer message (to the AI):**  
> You are an AI development orchestrator and coder.  
> You MUST strictly follow all rules and phases in `BLUEPRINT-Universal-1.1.md` (Research-Grade Package DNA with Mandatory Interactive Pipeline).  
>
> You are given:
> - `BLUEPRINT-Universal-1.1.md` – the governing process and quality standard.  
> - One or more proposal documents: either
>   - (a) a standardised `proposal.normalized.json`, or  
>   - (b) unstructured documents such as `Goal.docx`.  
>
> If you are given unstructured documents (case b):
> 1. Run **Phase -1 (Section 5.3)** using a three-expert panel (E1, E2, E3 under role R3, plus yourself as R1) to construct a unified, standardised `proposal.normalized.json`.
> 2. If three files are provided (Concept, Outline, Literature), map them explicitly:
>    - Concept -> Title/Scope/Objectives/Novelty/Risks,
>    - Outline -> `Methodology & Analysis Plan.steps[]` and all `manuscript_requirements` tables/figures,
>    - Literature -> `literature_context` for downstream BibTeX generation.
> 3. Expand every ordered methodology step into concrete task seeds in `tasks.seed.yaml`.
> 4. Ensure the resulting proposal passes the Definition of Ready (DoR) in Section 5.2.
> 5. If DoR fails, produce a clear validation report listing all issues and STOP.
>
> If you are given a standardised `proposal.normalized.json` (case a), or once you have produced one from Phase -1:
> 1. Start at **PHASE 0 (READ_PROPOSAL)**. Validate the proposal against the DoR.  
> 2. If the proposal is not ready, produce a validation report and STOP.  
> 3. If the proposal is ready, proceed through **PHASES 1A–6 in order** (Section 8):
>    - **Phase 1A**: Establish the agent team with `agents.yaml`,
>    - **Phase 1B**: Generate A1–A5 specs,  
>    - **Phase 2**: Build `tasks.yaml`,  
>    - **Phase 3**: Implement code and tests under `src/` and `tests/`,  
>    - **Phase 4**: Implement and test an interactive pipeline,  
>    - **Phase 5**: Produce governance artefacts (`TRACEABILITY.csv`, `DECISIONS.md`, `LITERATURE.bib`, `REPRODUCIBILITY.md`),  
>    - **Phase 6**: Run tests and CI scripts appropriate for this environment.
>
> Additional constraints:
> - Never skip phases, and do not modify the blueprint itself.  
> - Establish the agent team in Phase 1A before generating any specs.
> - Each agent may only use tools defined in their manifest.
> - Record major decisions into a `DECISIONS.md` file as described in the blueprint.  
> - Treat the interactive pipeline as a mandatory, first-class feature.

---

## Appendix A: Changelog

### Version 1.1-py (Python Edition - OO & Non-Coder Accessibility Focus)
- **Specialized blueprint for Python packages** following PEP standards with emphasis on OO design and non-coder usability
- Updated **Section 0** to specify:
  - Python-specific scope and PEP compliance
  - **Design Philosophy**: OO principles (encapsulation, inheritance, polymorphism, composition)
  - **Accessibility for Non-Coders**: No-code and minimal-code interface requirements
  - **Pythonic interactive console interface** as primary interaction model
- Updated **Section 2.1** proposal schema to include:
  - Python package specifics (pypi_name, import_name, dependencies, etc.)
  - **User experience & accessibility** fields (target user technical level, interface requirements)
- Added **Section 2.3** defining Python-specific package outputs (pyproject.toml, py.typed, etc.)
- Enhanced **Section 4 (A1-A5)** with Python-specific requirements:
  - A1: PyPI metadata, Python version compatibility
  - A2: Type hints (PEP 484), docstring formats (Google/NumPy/Sphinx)
  - A3: Package layout, dependency specifications, **OO architecture patterns** (class hierarchies, design patterns, composition)
  - A4: pytest configuration, fixtures, test markers, coverage
  - A5: Code quality tools (ruff, mypy, black), CI/CD with GitHub Actions, pre-commit hooks
- Added **Section 4.6 (A6) - User Experience & Non-Coder Accessibility** (NEW):
  - Target user profiles and personas
  - **Object-Oriented design patterns** (BaseModel ABC, encapsulation, composition, polymorphism)
  - **User-friendly interface** requirements (short function names, method chaining, rich output)
  - **IPython integration** (tab completion, rich display, interactive plots)
  - **Sensible defaults** and auto-detection
  - **User-friendly error messages** with suggestions
  - **Progressive disclosure** (simple → advanced → expert API levels)
  - Template scripts with clear modification sections
- Expanded **Section 7** with Python-specific mandatory tasks (pyproject.toml setup, type checking, build/distribution)
- Enhanced **Section 10** with **user-friendly interface patterns** (PRIMARY):
  - IPython/Python console with simple, readable commands
  - Interactive script mode with template files
  - De-emphasized web apps in favor of terminal-based interfaces
  - Jupyter notebooks as secondary (documentation/teaching only)
- Updated **Section 11.1** with Python environment setup, `uv` workflows, and dependency locking
- Updated **Section 11.2** with comprehensive GitHub Actions CI/CD example for Python
- Added **Section 11.3** Python Documentation Requirements (Sphinx, autodoc, docstrings, README, CHANGELOG)
- Expanded **Section 12** Final Acceptance Checklist to **31** items covering:
  - pyproject.toml validation
  - **User-friendly interface validation** (simple API, method chaining, rich output, IPython integration)
  - **OO design validation** (class hierarchies, ABCs, encapsulation, design patterns)
  - **Non-coder usability testing** (one-liner workflows, template scripts, error messages)
  - Package build and installation testing
  - PyPI metadata validation
  - Type checking and code quality
  - Documentation building (Sphinx) with non-coder friendly content
  - Versioning and release process
- Added **Appendix B** with comprehensive Python PEP references and standards:
  - Core PEPs (8, 257, 484, 586, 604)
  - Packaging PEPs (517, 518, 621, 440, 427, 561)
  - Language feature PEPs (3107, 526, 3119)
  - Tool configuration standards
  - Python version support guidelines
  - PEP compliance checklist

### Version 1.1
- Added **Phase 1A (ESTABLISH_AGENTS)** as a mandatory foundation phase
- Added **Section 6** defining agent configuration schema and tool manifests
- Added `agents.yaml` as a required output
- Updated phase numbering throughout (Phase 1 split into 1A and 1B)
- Added exit criteria to all phases in Section 8
- Enhanced TRACEABILITY.csv to include agent attribution
- Added agent boundary violation tracking to DECISIONS.md requirements
- Updated Final Acceptance Checklist to include agent configuration verification
- Updated quickstart prompts to include Phase 1A

### Version 1.0
- Initial release (language-agnostic)

---

## Appendix B: Python PEP References and Standards

This appendix lists the key Python Enhancement Proposals (PEPs) and standards that guide the Python-specific requirements in this blueprint.

### B.1 Core PEPs for Package Development

**PEP 8 – Style Guide for Python Code**
- URL: https://peps.python.org/pep-0008/
- Status: Active
- Covers: Naming conventions, code layout, indentation, imports, comments
- Relevance: All code MUST follow PEP 8 conventions unless explicitly justified

**PEP 257 – Docstring Conventions**
- URL: https://peps.python.org/pep-0257/
- Status: Active
- Covers: Docstring format, placement, content
- Relevance: All public modules, functions, classes, and methods MUST have docstrings

**PEP 484 – Type Hints**
- URL: https://peps.python.org/pep-0484/
- Status: Accepted
- Covers: Function annotations, type comments, typing module
- Relevance: All public APIs SHOULD include type hints

**PEP 586 – Literal Types**
- URL: https://peps.python.org/pep-0586/
- Status: Accepted
- Covers: `Literal[]` for exact value typing
- Relevance: Use for string literals, enums, and constant values

**PEP 604 – Allow writing union types as X | Y**
- URL: https://peps.python.org/pep-0604/
- Status: Accepted (Python 3.10+)
- Covers: Union type syntax (`int | str` instead of `Union[int, str]`)
- Relevance: Preferred for Python 3.10+ packages

### B.2 Packaging and Distribution PEPs

**PEP 517 – A build-system independent format for source trees**
- URL: https://peps.python.org/pep-0517/
- Status: Final
- Covers: `pyproject.toml` `[build-system]` section
- Relevance: MUST specify build backend in `pyproject.toml`

**PEP 518 – Specifying Minimum Build System Requirements**
- URL: https://peps.python.org/pep-0518/
- Status: Final
- Covers: `pyproject.toml` as configuration file
- Relevance: MUST use `pyproject.toml` as primary metadata file

**PEP 621 – Storing project metadata in pyproject.toml**
- URL: https://peps.python.org/pep-0621/
- Status: Final
- Covers: `[project]` section structure, metadata fields
- Relevance: MUST define package metadata in `[project]` section

**PEP 440 – Version Identification and Dependency Specification**
- URL: https://peps.python.org/pep-0440/
- Status: Active
- Covers: Version numbering scheme, version specifiers for dependencies
- Relevance: Version numbers and dependency constraints MUST follow PEP 440

**PEP 427 – The Wheel Binary Package Format**
- URL: https://peps.python.org/pep-0427/
- Status: Final
- Covers: `.whl` file format for distribution
- Relevance: Packages MUST be distributable as wheels

**PEP 561 – Distributing and Packaging Type Information**
- URL: https://peps.python.org/pep-0561/
- Status: Accepted
- Covers: `py.typed` marker file for typed packages
- Relevance: If package includes type hints, MUST include `py.typed`

### B.3 Language Feature PEPs

**PEP 3107 – Function Annotations**
- URL: https://peps.python.org/pep-3107/
- Status: Final
- Covers: Syntax for function annotations
- Relevance: Foundation for type hints (PEP 484)

**PEP 526 – Syntax for Variable Annotations**
- URL: https://peps.python.org/pep-0526/
- Status: Final
- Covers: Variable type annotations
- Relevance: Use for class attributes and module-level variables

**PEP 3119 – Introducing Abstract Base Classes**
- URL: https://peps.python.org/pep-3119/
- Status: Final
- Covers: `abc` module, `ABC` base class
- Relevance: Use for defining interfaces and abstract methods

### B.4 Tool-Specific Standards

**PEP 518 / pyproject.toml tool configuration**
- Most modern Python tools support configuration in `pyproject.toml`
- Standard sections:
  - `[tool.ruff]` – Ruff linter/formatter
  - `[tool.black]` – Black formatter
  - `[tool.mypy]` – Mypy type checker
  - `[tool.pytest.ini_options]` – Pytest configuration
  - `[tool.coverage.run]` – Coverage.py configuration
  - `[tool.isort]` – Import sorting (if not using ruff)

### B.5 Additional References

**Python Packaging User Guide (PyPA)**
- URL: https://packaging.python.org/
- Covers: Comprehensive guide to Python packaging
- Relevance: Authoritative source for packaging best practices

**Python Developer's Guide**
- URL: https://devguide.python.org/
- Covers: Contributing to CPython, core development
- Relevance: Style and conventions used in standard library

**NumPy Docstring Guide**
- URL: https://numpydoc.readthedocs.io/
- Covers: NumPy-style docstring format
- Relevance: Common in scientific Python packages

**Google Python Style Guide**
- URL: https://google.github.io/styleguide/pyguide.html
- Covers: Google's Python conventions and docstring format
- Relevance: Alternative docstring style option

**Keep a Changelog**
- URL: https://keepachangelog.com/
- Covers: Changelog format and best practices
- Relevance: CHANGELOG.md SHOULD follow this format

**Semantic Versioning**
- URL: https://semver.org/
- Covers: Version numbering convention (MAJOR.MINOR.PATCH)
- Relevance: Package versions SHOULD follow semantic versioning

### B.6 PEP Status Definitions

Understanding PEP status is important when deciding which features to use:

- **Draft**: Work in progress, may change significantly
- **Accepted**: Approved, will be implemented or is being implemented
- **Final**: Completed and implemented in Python
- **Active**: Informational PEP that is continually updated (like PEP 8)
- **Provisional**: Tentatively accepted, may still be revised
- **Rejected**: Proposal was rejected
- **Withdrawn**: Proposal was withdrawn by author
- **Superseded**: Replaced by another PEP

### B.7 Python Version Support Guidelines

When choosing minimum Python version:

- **Python 3.9** (Oct 2020, EOL Oct 2025): Minimum for most new packages
  - Dict merge operator (`|`), type hint improvements
- **Python 3.10** (Oct 2021, EOL Oct 2026): Good default for new projects
  - Pattern matching, union type operator (`X | Y`)
- **Python 3.11** (Oct 2022, EOL Oct 2027): Best performance
  - Significant speed improvements, better error messages
- **Python 3.12** (Oct 2023, EOL Oct 2028): Latest stable
  - Further performance gains, improved type hints

**Recommendation**: Set minimum to Python 3.9 or 3.10 for broad compatibility, test up to 3.12+

### B.8 Compliance Checklist for PEPs

A compliant package MUST:
- ✓ Follow PEP 8 style (enforced by ruff/flake8)
- ✓ Use PEP 440 version specifiers
- ✓ Define metadata per PEP 621 in `pyproject.toml`
- ✓ Specify build system per PEP 517/518

A compliant package SHOULD:
- ✓ Include type hints (PEP 484)
- ✓ Include `py.typed` if typed (PEP 561)
- ✓ Write docstrings (PEP 257)
- ✓ Use semantic versioning

A compliant package MAY:
- Use modern syntax features (PEP 604, PEP 526) if min Python version supports it
- Include abstract base classes (PEP 3119) for extensibility
