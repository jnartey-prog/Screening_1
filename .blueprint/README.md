# Universal Blueprint System

This directory contains the **Universal Blueprint System** for autonomous software development. It allows **any AI agent** (Gemini, Claude, GPT-4, Llama 3) to build high-quality Python packages by following standard roles and skills.

## Structure

- **`config.yaml`**: Configuration for the blueprint version and active roles.
- **`state.json`**: Tracks the current progress of the build (Agent Memory).
- **`tools.json`**: Defines the abstract tools required (MCP-compatible).
- **`roles/`**: System prompts for each role (R1-R7). Load these to "become" a specific expert.
- **`skills/`**: Executable workflows for each step of the process.
  - Includes `idea_to_proposal.md` for Phase -1 document-to-proposal normalization.
  - Includes `plot_publication_artifacts.md` for publication-grade table/figure generation.

## How to Use

### For AI Agents
1.  **Read Config:** Start by reading `.blueprint/config.yaml`.
2.  **Read State:** Check `.blueprint/state.json` to see what needs to be done.
3.  **Load Role:** Load the appropriate role prompt from `.blueprint/roles/` (e.g., `R1_Orchestrator.md`).
4.  **Execute Skill:** Follow the instructions in the active skill file (e.g., `.blueprint/skills/orchestrator.md`).

### For Humans
To start a new project:
```bash
# Initialize the blueprint (if you haven't already)
# (These files are already created for you in this project)
```

To run the build:
1.  Ask your AI agent: *"Please act as the R1 Orchestrator. Read `.blueprint/skills/orchestrator.md` and start the build process."*

## Roles
- **R1 - Orchestrator**: Project Manager.
- **R2 - Architect**: Technical design.
- **R3 - Domain Scientist**: Scientific validity.
- **R4 - Implementer**: Coding.
- **R5 - Tester**: QA.
- **R6 - Documenter**: Docs & UX.
- **R7 - RPM**: Governance.
