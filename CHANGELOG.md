# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-08-05

This release introduces comprehensive multi-model support (Google Gemini, Anthropic Claude, and OpenAI/Codex) alongside dynamic LLM veracity controls (temperature configurations) in the settings panel.

### Added
- **Multi-Model Support**: Integrated Gemini (Pro, Flash, and Free Developer Tier), Anthropic Claude (Sonnet, Haiku), and OpenAI/Codex (GPT-4o, GPT-4o-mini).
- **Dynamic API Key Config**: Settings menu dynamically displays Google, Anthropic, and/or OpenAI API key inputs depending on the selected model to reduce configuration complexity.
- **Veracity & Accuracy Levels**: Set LLM temperature via a new interactive selection menu:
  - *Strict/Deterministic* (Temp: 0.0) for rigorous bug audits.
  - *Balanced* (Temp: 0.4) for standard feedback.
  - *Creative* (Temp: 0.7) for alternative coding ideas.
- **Under the Hood Integration**: Passes temperature dynamically to the entire multi-agent pipeline using Google GenAI SDK's `GenerateContentConfig`.

## [1.1.0] - 2026-08-05

This release introduces a fully interactive, modernized console UI with keyboard navigation, custom ANSI coloring, and multi-language support (English/Spanish).

### Added
- **Interactive Keyboard Navigation**: Use Up/Down arrows to navigate options, and Enter to select.
- **Modern ANSI Styling**: Added cyber cyan headers, green cursors, gray shortcuts, and bold layouts.
- **Multilingual Support (i18n)**: Switch the entire interface dynamically between Spanish and English. Preference is persisted via `CLI_LANG` in `.env`.
- **Keyboard Shortcuts**: Directly execute options by pressing numbers `1-5`, or press `Esc` / `q` to exit.
- **Piping Fallback (isatty check)**: Automatically falls back to traditional text input if stdout/stdin are piped, maintaining full test suite compatibility.

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
