# Project Harness: HTML Branching Rule System (Google Harness² Applied)

This workspace implements an **HTML-based hierarchical branching rule system** for AI coding tools and humans, governed by **Google Harness²** (`google-research/harness2`, arXiv:2610.14224).

## 1. Standing Invariants (Always-On)
- **Minimal Context First**: Never read CSS, JS, or unrelated rule branches into AI context. Read `rules/router.html` (or run `scripts/resolve_rule.py`) and load ONLY the active branch chain inside `<!-- AI-RULE-START --> ... <!-- AI-RULE-END -->`.
- **Dual-Audience HTML**: Every rule node in `rules/` is human-readable styled HTML (via external `rules/assets/rule-ui.css` and `rule-ui.js`) while exposing compact semantic `data-*` attributes for zero-bloat AI routing.
- **Difficulty-Aware Routing**: Every non-trivial task is routed to a capability tier (`low`, `mid`, `high`), reasoning effort (`low`, `medium`, `high`), adaptation policy (`effort-first-with-verifier`, `capacity-switch-sensitive`, `grounding-over-thinking`, `overthinking-guard-low`), and required skills—choosing whether to raise effort or switch models based on empirical triggers. Model names listed in the catalog are non-exhaustive reference examples; always map `(tier, effort)` to the models/parameters supported by the user's current tool/environment, and treat rules as general baselines whose realized cost/quality varies by task specifics.
- **No Unverified Claims / Safety**: Ask the user ONLY before deleting files, rebooting, or when external login/credits block progress.
- **Session Handoff Threshold (80% Context)**: If session context exceeds 80%, write `tradeoff.md`, update `progress.md` and `reference.md`, and instruct the next session to load `AGENTS.md`, `rules.md`, `reference.md`, `progress.md`, and `tradeoff.md`.

## 2. Skill Triggers (On-Demand — Load Only When Matched)
- When routing a task through the HTML rule tree, estimating task difficulty, or recommending a model tier (`low`/`mid`/`high`), effort, and skills, read `.agents/skills/rule-router/SKILL.md` and follow it.
- When proposing, probing, or composing custom HTML rule branches or updating the experience library, read `.agents/skills/harness-propose-probe-compose/SKILL.md` and follow it.
- When performing low-tier claim checking, logical argument generation, or multi-source citation verification, read `.agents/skills/claim-verify/SKILL.md` and follow it.
- When debugging errors, analyzing stack traces, or writing targeted code patches, read `.agents/skills/targeted-debug/SKILL.md` and follow it.
- When designing multi-module architecture, performing refactors, or resolving concurrency/security tradeoffs, read `.agents/skills/architecture-rfc/SKILL.md` and follow it.
- When selecting or combining Prompt, Context, Harness, Loop, or Graph architectures for AI system use cases, read `.agents/skills/ai-architecture-stack/SKILL.md` and follow it.
- When targeting top/frontier models for exceptional visual/creative deliverables or running anti-slop screenshot critique loops, read `.agents/skills/frontier-craft/SKILL.md` and follow it.
- When importing, auditing, or vetting third-party/untrusted skills for prompt injection or exfiltration risks, read `.agents/skills/skill-security-audit/SKILL.md` and follow it.

## 3. Deterministic Helpers & Key Files
- `python scripts/resolve_rule.py --task "<prompt>"` — resolves active HTML branch path, minimal AI rule packet, model tier, effort, and skills.
- `python scripts/validate_harness.py` — validates Harness² surface caps, skill triggers, HTML node schema, skill security gate, and syncs `rules/assets/tree-data.js`.
- `python scripts/scan_skills_security.py` — static security scanner blocking malicious/injected `SKILL.md` or bundled scripts.
- `rules.md` — full project governance protocol (Steps 1–8, Liner Scholar credit guard, fallback loop).
- `reference.md` & `reference/` — verified GitHub repos, web docs, and Liner Scholar papers.
- `progress.md` — milestone log and verification state; `library/INDEX.md` — Harness² experience library.
