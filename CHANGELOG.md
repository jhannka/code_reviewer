# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-08-05

This is the first official release of the Multi-Agent Code Reviewer agent, featuring a decoupled Hexagonal Architecture layout and a sequential 6-agent analysis pipeline.

### Added

* **Specialized Multi-Agent Pipeline**:
  * Coordinator agent to orchestrate the workflow.
  * `skills_explorer` to index design guidelines.
  * `change_finder` to retrieve git modifications.
  * `error_analyzer` to inspect code discrepancies.
  * `refactoring_advisor` to propose modifications and incremental refactoring plans.
  * `change_applier` to apply edits step-by-step.
  * `test_executor` to run pytest verifications.
* **Hexagonal Architecture Implementation**:
  * Isolated core use cases (`CodeReviewToolsService`) from I/O ports.
  * Built adapters for local filesystem, git VCS, home directory skills path resolution, and subprocess unit test runner.
* **Global CLI Portability**:
  * `bin/code-reviewer` (bash) and `bin/code-reviewer.bat` (cmd) global wrappers.
  * `install.sh` installation script for automatic `/usr/local/bin` symbolic linking.
* **Console UI spinners**:
  * Real-time loading indicator and callback signals (`before_agent`, `after_agent`) to display active agent execution.
* **Documentation**:
  * Scannable English `README.md` with system dependencies, execution guidelines, CLI options walkthrough, and visual mermaid sequence diagram.
  * Automated testing configuration with `pytest` mocks verifying adapter and domain ports.
