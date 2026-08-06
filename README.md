# Multi-Agent Code Reviewer (Hexagonal Architecture)

A CLI-based code reviewer application built with **Google ADK (Agent Development Kit)**. It coordinates a sequential pipeline of 6 specialized AI agents to analyze, propose, apply, and verify code changes based on project-specific design rules (skills). The codebase is structured using **Hexagonal Architecture** for dynamic path resolution, dependency injection, and clean unit testing.

---

## Quick Path

### 0. System Dependencies

Before setting up the project, ensure you have **Python 3.10+**, **Node.js 18+**, and **Git** installed on your operating system:

| Platform | Installation Method |
|----------|---------------------|
| **macOS** | Install via [Homebrew](https://brew.sh):<br>`brew install python git node` |
| **Linux (Ubuntu/Debian)** | Install via `apt`:<br>`sudo apt update && sudo apt install -y python3 python3-venv git nodejs npm` |
| **Windows** | Install via `winget` (or download official installers):<br>`winget install Python.Python.3.11`<br>`winget install Git.Git`<br>`winget install OpenJS.NodeJS` |

### 1. Install dependencies:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install google-adk python-dotenv pytest
   npm install
   ```
2. **Configure environment secrets**:
   Copy the environment variables template and add your Gemini API key:
   ```bash
   cp code_reviewer/.env.example code_reviewer/.env
   # Edit code_reviewer/.env and set your GOOGLE_API_KEY
   ```
3. **Launch the CLI**:
   ```bash
   npm run menu   # Or alternatively: python3 menu.py
   ```
4. **Run verification tests**:
   ```bash
   PYTHONPATH=.:code_reviewer .venv/bin/pytest
   ```

---

## Specialized Agent Pipeline

The execution flow is coordinated sequentially by a central **`coordinator_agent`** which delegates tasks to the following specialized agents:

```mermaid
graph TD
    Start([User Request]) --> Coordinator[Coordinator Agent]
    Coordinator --> A1[1. Skills Explorer]
    A1 --> A2[2. Change Finder]
    A2 --> A3[3. Error Analyzer]
    A3 --> A4[4. Refactoring Advisor]
    A4 --> Coordinator
    Coordinator -->|User Approval| A5[5. Change Applier]
    A5 --> A6[6. Test Executor]
    A6 --> End([Result Summary])
```

1. **`skills_explorer`**: Reads and indexes global and local design guidelines (`read_project_skills`).
2. **`change_finder`**: Detects git status/diff and reads source code files (`get_git_changes`, `read_source_file`).
3. **`error_analyzer`**: Compares files against design guidelines to identify syntax bugs, logic errors, and structural deviations.
4. **`refactoring_advisor`**: Generates a refactoring proposal. If the changes are extensive (exceeding 50 lines of code or spanning multiple files), it designs a step-by-step **Incremental Refactoring Plan** so modifications can be verified incrementally.
5. **`change_applier`**: Modifies files on the filesystem (`write_source_file`) following the proposal or step-by-step incremental plan.
6. **`test_executor`**: Executes the test suite via the test runner adapter (`execute_unit_tests`) to verify correctness after changes.

---

## Architectural Layout

The project uses **Hexagonal Architecture** to decouple the core logic from external dependencies (I/O, VCS, shell executions):

| Component | Directory | Description |
|-----------|-----------|-------------|
| **Domain** | [`code_reviewer/domain/`](file:///Users/jhanncarlos/Documents/App/My%20Apps/code_reviewer/code_reviewer/domain) | Contains `CodeReviewToolsService` implementing pure domain use cases without system references. |
| **Ports** | [`code_reviewer/ports/`](file:///Users/jhanncarlos/Documents/App/My%20Apps/code_reviewer/code_reviewer/ports) | Defines secondary ports (`driven.py`, `test_runner.py`) and primary ports (`driving.py`). |
| **Adapters (Driven)** | [`code_reviewer/adapters/driven/`](file:///Users/jhanncarlos/Documents/App/My%20Apps/code_reviewer/code_reviewer/adapters/driven) | Concrete implementations for infrastructure (Git VCS, Pytest subprocess executing, OS FileSystem, and dynamic skills path expansion relative to the home directory). |
| **Adapters (Driving)** | [`code_reviewer/adapters/driving/`](file:///Users/jhanncarlos/Documents/App/My%20Apps/code_reviewer/code_reviewer/adapters/driving) | Facade wrapping tool executions with schemas matching ADK requirements (`tool_facade.py`). |
| **Composition Root** | [`code_reviewer/agent.py`](file:///Users/jhanncarlos/Documents/App/My%20Apps/code_reviewer/code_reviewer/agent.py) | Wire-up entrypoint connecting ports, adapters, and instantiating the specialized agents and coordinator loop. |

---

## Verification Checklist

- [ ] Unit tests pass cleanly in local environments (`6/6 passed`).
- [ ] Staging and environment credentials are separated (secrets ignored via `.gitignore`).
- [ ] No hardcoded absolute home directories are present.
- [ ] The CLI starts up without module resolution or path import issues.

---

## Next Steps

To add new design directives for the agents to enforce:
Create a markdown rules file (e.g., `MY_GUIDELINE_SKILL.md`) inside the global directory `~/.gemini/config/skills/` or a local directory `.agents/skills/`. The `skills_explorer` agent will automatically detect and apply the new guidelines in the next execution turn.
