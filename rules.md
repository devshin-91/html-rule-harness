# Project Rules & Governance Protocol (`rules.md`)

This document specifies the standing project governance rules built on **Google Harness²** (`google-research/harness2`, arXiv:2610.14224). Keep `AGENTS.md` lean and always-on; read this file on demand when auditing workflow compliance or handing off a session.

## 1. Harness Framework (Google Harness²)
- **Architecture**: Apply Harness²'s component discipline (`AGENTS.md` always-on <= 8,000 chars, `.agents/skills/<name>/SKILL.md` on-demand with verbatim triggers in `AGENTS.md`, deterministic helpers in `scripts/*.py`, delegated `sub_agents/*/AGENT.md` when needed, and a persistent experience library in `library/`).
- **Two-Level Recursion**:
  1. *Task-Level (Propose–Probe–Compose)*: Propose HTML branch structures or edits, probe them with `scripts/resolve_rule.py` and `scripts/validate_harness.py` (measuring token savings, routing precision, and HTML UI integrity), and compose the winning minimal structure.
  2. *Harnessing-Level (Experience Library)*: Record validated cues, lessons, and empirical evidence in `library/INDEX.md` and `library/EXPERIENCE.md`.

## 2. GitHub Repository Discovery
- Search and inspect both widely adopted and specialized GitHub repositories relevant to agent rules, progressive disclosure, `AGENTS.md`, skills, and difficulty-based model routing before finalizing designs.

## 3. Web Docs & Liner Scholar Paper Search (Credit Guard)
- Search authoritative web documentation (Antigravity docs, `agentskills.io`, `agents.md`, arXiv) and use **Liner Scholar** (`https://scholar.liner.com/`) via the built-in browser.
- **Strict Liner Scholar Credit Guard**: Before *every* Liner Scholar query or credit-consuming action, verify the user's current credit balance. If the remaining balance is **<= 100 credits**, **stop immediately** without running the query. Proceed only when verified **> 100 credits**.

## 4. Reference Organization (`reference/` & `reference.md`)
- Document every reference that genuinely informed design or implementation inside `reference/` as structured Markdown files, indexed in `reference.md`.

## 5. Progress Tracking (`progress.md`)
- Maintain and save `progress.md` upon completion of major phases and at project completion, listing completed artifacts, verification outputs, and next actions.

## 6. Blocker Resolution Loop (Updated Rule 6)
- Whenever blocked during implementation or design, **re-apply Steps 2–5**:
  - (Step 2) Explore popular/useful GitHub repos,
  - (Step 3) Check web docs & Liner Scholar (checking credit balance > 100 first),
  - (Step 4) Systematize helpful findings in `reference/`,
  - (Step 5) Record updates in `progress.md`.

## 7. Minimal Interruption Policy
- Proceed autonomously without unnecessary questions. Ask the user **only** when file/resource deletion, system reboot, or external authentication/blockers (e.g. login or low credits) require user intervention.

## 8. Session Context Handoff (> 80% Context Window)
- If conversation context exceeds **80%** of the context window:
  1. Create/update `tradeoff.md` documenting key architectural decisions, rejected alternatives, open risks, and next steps.
  2. Ensure `AGENTS.md`, `rules.md`, `reference.md`, `progress.md`, and `tradeoff.md` are saved on disk.
  3. Instruct the new session to read `AGENTS.md`, `rules.md`, `reference.md`, `progress.md`, and `tradeoff.md` immediately so it inherits the exact Harness² setup and full state.
