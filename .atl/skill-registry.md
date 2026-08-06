# Skill Registry

This registry index contains all global, plugin, and project-level skills available to the agent.

| Skill Name | Scope | Trigger / Description | File Path |
|------------|-------|-----------------------|-----------|
| **_shared** | `global` | Shared SDD references for installed skills. Not invokable. | [_shared/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/_shared/SKILL.md) |
| **a11y-debugging** | `plugin` | testing semantic HTML, ARIA labels, focus states, keyboard navigation, tap targets, and color contrast. | [a11y-debugging/SKILL.md](file:///Users/jhanncarlos/.gemini/config/plugins/chrome-devtools-plugin/skills/a11y-debugging/SKILL.md) |
| **branch-pr** | `global` | creating, opening, or preparing PRs for review. | [branch-pr/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/branch-pr/SKILL.md) |
| **chained-pr** | `global` | PRs over 400 lines, stacked PRs, review slices. Split oversized changes into chained PRs that protect review focus. | [chained-pr/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/chained-pr/SKILL.md) |
| **chrome-devtools** | `plugin` | debugging web pages, automating browser interactions, analyzing performance, or inspecting network requests. This skill does not apply to `--slim` mode (MCP configuration). | [chrome-devtools/SKILL.md](file:///Users/jhanncarlos/.gemini/config/plugins/chrome-devtools-plugin/skills/chrome-devtools/SKILL.md) |
| **cognitive-doc-design** | `global` | writing guides, READMEs, RFCs, onboarding, architecture, or review-facing docs. | [cognitive-doc-design/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/cognitive-doc-design/SKILL.md) |
| **comment-writer** | `global` | PR feedback, issue replies, reviews, Slack messages, or GitHub comments. | [comment-writer/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/comment-writer/SKILL.md) |
| **debug-optimize-lcp** | `plugin` | the user mentions "largest contentful paint", "page load speed", "CWV", or wants to improve how fast their hero image or main content renders. | [debug-optimize-lcp/SKILL.md](file:///Users/jhanncarlos/.gemini/config/plugins/chrome-devtools-plugin/skills/debug-optimize-lcp/SKILL.md) |
| **go-testing** | `global` | Go tests, go test coverage, Bubbletea teatest, golden files. Apply focused Go testing patterns. | [go-testing/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/go-testing/SKILL.md) |
| **issue-creation** | `global` | creating GitHub issues, bug reports, or feature requests. | [issue-creation/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/issue-creation/SKILL.md) |
| **judgment-day** | `global` | judgment day, dual review, adversarial review, juzgar. Run explicit blind dual review with at most two scoped fix/re-judgment rounds. | [judgment-day/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/judgment-day/SKILL.md) |
| **memory-leak-debugging** | `plugin` | a user reports high memory usage, OOM errors, or wants to analyze heapsnapshots or run memory leak detection tools like memlab. | [memory-leak-debugging/SKILL.md](file:///Users/jhanncarlos/.gemini/config/plugins/chrome-devtools-plugin/skills/memory-leak-debugging/SKILL.md) |
| **sdd-apply** | `global` | orchestrator launches apply for one or more change tasks. | [sdd-apply/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-apply/SKILL.md) |
| **sdd-archive** | `global` | orchestrator launches archive after implementation and verification. | [sdd-archive/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-archive/SKILL.md) |
| **sdd-design** | `global` | orchestrator launches design for a change. | [sdd-design/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-design/SKILL.md) |
| **sdd-explore** | `global` | orchestrator launches exploration or requirement clarification. | [sdd-explore/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-explore/SKILL.md) |
| **sdd-init** | `global` | sdd init, iniciar sdd, openspec init. Initialize SDD context, testing capabilities, registry, and persistence. | [sdd-init/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-init/SKILL.md) |
| **sdd-onboard** | `global` | orchestrator launches onboarding for the full SDD cycle. | [sdd-onboard/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-onboard/SKILL.md) |
| **sdd-propose** | `global` | orchestrator launches proposal work for a change. | [sdd-propose/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-propose/SKILL.md) |
| **sdd-spec** | `global` | orchestrator launches spec work for a change. | [sdd-spec/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-spec/SKILL.md) |
| **sdd-tasks** | `global` | orchestrator launches task planning for a change. | [sdd-tasks/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-tasks/SKILL.md) |
| **sdd-verify** | `global` | SDD verification phase, verify change. Execute tests and prove implementation matches specs, design, and tasks. | [sdd-verify/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/sdd-verify/SKILL.md) |
| **skill-creator** | `global` | new skills, agent instructions, documenting AI usage patterns. Create LLM-first skills with valid frontmatter. | [skill-creator/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/skill-creator/SKILL.md) |
| **skill-improver** | `global` | improve skills, audit skills, refactor skills, skill quality. Audit and upgrade existing LLM-first skills. | [skill-improver/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/skill-improver/SKILL.md) |
| **skill-registry** | `global` | update skills, skill registry, actualizar skills, after skill changes. Index available skills by trigger and path. | [skill-registry/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/skill-registry/SKILL.md) |
| **troubleshooting** | `plugin` | Uses Chrome DevTools MCP and documentation to troubleshoot connection and target issues. Trigger this skill when list_pages, new_page, or navigate_page fail, or when the server initialization fails. | [troubleshooting/SKILL.md](file:///Users/jhanncarlos/.gemini/config/plugins/chrome-devtools-plugin/skills/troubleshooting/SKILL.md) |
| **work-unit-commits** | `global` | implementation, commit splitting, chained PRs, or keeping tests and docs with code. | [work-unit-commits/SKILL.md](file:///Users/jhanncarlos/.gemini/config/skills/work-unit-commits/SKILL.md) |
