# Project Harness: MD-Source → HTML-Compiled Branching Rule System v2.0 (Google Harness² Applied)

This workspace implements a **v2.0 Markdown-Source → HTML-Compiled hierarchical branching rule system** for AI coding tools and humans, governed by **Google Harness²** (`google-research/harness2`, arXiv:2610.14224), **MD-vs-HTML Single-Source-of-Truth (`md-html-guide`)**, and **5-Lineage Anti-Hallucination Guardrails (`antigravity-gemini-anti-hallucination`)**.

## 1. Standing Invariants (Always-On)
- **MD Single Source of Truth → Deterministic HTML Views**: Authoritative rule definitions live in `rules/src/router.md` and `rules/src/branches/**/*.md` (Markdown + YAML frontmatter). `scripts/build_rules_html.py` deterministically compiles them (0 LLM tokens) into `rules/router.html`, `rules/branches/**/*.html`, and `rules/assets/tree-data.js` for human review. Never hand-edit compiled HTML; edit `rules/src/**/*.md` and recompile.
- **Minimal Context First**: Never read CSS, JS, or human HTML dashboards (`rules/index.html`) into AI context. Run `python scripts/resolve_rule.py --task "<prompt>"` (reads `rules/src/**/*.md` primary with HTML fallback) and load ONLY the active branch chain packet.
- **Tool-First Anti-Hallucination Guard**: Never rely on parametric memory for model/API/SDK specs or dismiss newer models/versions (no reverse hallucination). Verify via local files/official docs/runtime execution first, quote verbatim with `#Lstart-Lend` line ranges before conclusions, abstain when absent, reject false premises with counterexamples, and execute code/tests before claiming done.
- **Difficulty-Aware Routing (`model-catalog.json` v3.0)**: Every non-trivial task is routed to a capability tier (`low`, `mid`, `high`), reasoning effort (`low`, `medium`, `high`), adaptation policy (`effort-first-with-verifier`, `capacity-switch-sensitive`, `grounding-over-thinking`, `overthinking-guard-low`), and required skills. Model names in the catalog (e.g., Gemini 3.5 Flash-Lite / Decisions API, Gemini 4 Hydrogen / Neon, Gemini 4 Argon / Carbon) are non-exhaustive reference examples; always map `(tier, effort)` to the models/parameters supported by the user's runtime and respect exact per-model `thinking_level` and Long Decode rules.
- **No Unverified Claims / Safety**: Ask the user ONLY before deleting files, rebooting, or when external login/credits block progress.
- **Session Handoff Threshold (80% Context)**: If session context exceeds 80%, write `tradeoff.md`, update `progress.md` and `reference.md`, and instruct the next session to load `AGENTS.md`, `rules.md`, `reference.md`, `progress.md`, and `tradeoff.md`.

## 2. Skill Triggers (On-Demand — Load Only When Matched)
- When routing a task through the branching rule tree, estimating task difficulty, or recommending a model tier (`low`/`mid`/`high`), effort, and skills, read `.agents/skills/rule-router/SKILL.md` and follow it.
- When proposing, probing, or composing custom rule branches (`rules/src/**/*.md` → compiled HTML) or updating the experience library, read `.agents/skills/harness-propose-probe-compose/SKILL.md` and follow it.
- When performing low-tier claim checking, logical argument generation, or multi-source citation verification, read `.agents/skills/claim-verify/SKILL.md` and follow it.
- When debugging errors, analyzing stack traces, or writing targeted code patches, read `.agents/skills/targeted-debug/SKILL.md` and follow it.
- When designing multi-module architecture, performing refactors, or resolving concurrency/security tradeoffs, read `.agents/skills/architecture-rfc/SKILL.md` and follow it.
- When selecting or combining Prompt, Context, Harness, Loop, or Graph architectures for AI system use cases, read `.agents/skills/ai-architecture-stack/SKILL.md` and follow it.
- When targeting top/frontier models for exceptional visual/creative deliverables or running anti-slop screenshot critique loops, read `.agents/skills/frontier-craft/SKILL.md` and follow it.
- When importing, auditing, or vetting third-party/untrusted skills for prompt injection or exfiltration risks, read `.agents/skills/skill-security-audit/SKILL.md` and follow it.
- When auditing model/API/SDK specs, verifying factual citations, preventing reverse hallucination or partial patches, or enforcing 5-lineage guardrails (Flash/Lite, Hydrogen, Neon, Argon, Carbon), read `.agents/skills/anti-hallucination-guard/SKILL.md` and follow it.

## 3. Deterministic Helpers & Key Files
- `python scripts/build_rules_html.py` (`--check`) — deterministically compiles `rules/src/**/*.md` into `rules/router.html`, `rules/branches/**/*.html`, and `rules/assets/tree-data.js` (fails non-zero if out of sync).
- `python scripts/resolve_rule.py --task "<prompt>"` — resolves active branch path from `rules/src/**/*.md` (HTML fallback), minimal AI rule packet (XML/JSON/MD), model tier, effort, and skills.
- `python scripts/validate_harness.py` — validates Harness² surface caps (`AGENTS.md <= 8,000` chars), skill triggers, MD-to-HTML compile sync, node schema, and skill security gate.
- `python scripts/scan_skills_security.py` — static security scanner blocking malicious/injected `SKILL.md` or bundled scripts.
- `rules.md` — full project governance protocol; `reference.md` & `reference/` — verified repos, docs, and papers; `progress.md` — milestone log; `library/INDEX.md` — Harness² experience library.
