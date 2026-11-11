---
name: harness-propose-probe-compose
description: Apply Google Harness² two-level recursion (Propose-Probe-Compose and Experience Library updates) to build, split, or refine custom HTML rule branches without bloating always-on context. Use when creating custom task branches or optimizing rule context efficiency.
---

# Harness² Propose–Probe–Compose for HTML Rule Trees

## Task-Level Recursion (Propose–Probe–Compose)
1. **Propose**:
   - Identify recurring friction or a specialized task domain requiring finer branching.
   - Split an overly broad HTML branch node into targeted child HTML files under `rules/branches/<domain>/`.
   - Keep each node's `<!-- AI-RULE-START --> ... <!-- AI-RULE-END -->` block concise (target <= 900 bytes, hard cap 1,800 bytes) with external CSS/JS links only.
   - Set explicit `data-tier`, `data-effort`, `data-skills`, and `data-escalate-when` attributes.
2. **Probe**:
   - Run `python scripts/validate_harness.py` to check Harness² surface caps, HTML node schema, parent/child graph integrity, and auto-sync `rules/assets/tree-data.js`.
   - Run `python scripts/resolve_rule.py --task "<probe query>" --json` across representative test prompts (low/mid/high complexity) and verify:
     - Correct branch selected,
     - Correct model tier + effort + skills proposed,
     - Active rule tokens <= 15% of total rule tree tokens.
3. **Compose**:
   - Keep only rules supported by observed probe contrasts; trim redundant prose.

## Harnessing-Level Recursion (Experience Library)
- Append validated lessons (`cue`, `lesson`, `evidence`, `confidence`) to `library/EXPERIENCE.md` and update `library/INDEX.md`.
