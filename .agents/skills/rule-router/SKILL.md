---
name: rule-router
description: Navigate the HTML branching rule tree, minimize rule context loaded into the prompt, and recommend the optimal model tier (low/mid/high), reasoning effort, and skills for a task. Use whenever classifying a new task, exploring branches in rules/, or checking escalation criteria.
---

# Rule Router (Minimal-Context HTML Branch Explorer)

## Goal
Resolve the single most specific HTML rule branch for the current task while keeping rule context overhead minimal (< 500 tokens).

## Protocol
1. **Never load CSS, JS, or unrelated branch files**: Ignore `rules/assets/*` and `rules/index.html` UI markup during AI execution.
2. **Fast Path (Deterministic Resolver)**:
   Run:
   `python scripts/resolve_rule.py --task "<concise task summary>"`
   Add `--no-verifier` when no automated tests/compiler/linter oracle exists (forces model switch earlier at Modal Ceiling instead of blind effort retries).
   or if you already know the branch ID:
   `python scripts/resolve_rule.py --branch <branch.id>`
3. **Manual HTML Traversal Path (No Shell Needed)**:
   - Step A: Read ONLY lines within `<!-- AI-RULE-START -->` ... `<!-- AI-RULE-END -->` of `rules/router.html`.
   - Step B: Match the task against `<a href="..." data-when="...">` links and open ONLY the single matching child `.html` file.
   - Step C: Repeat until reaching a leaf node (or stop at the deepest matching branch).
4. **Apply Model Tier, Effort & Skill Recommendations**:
   - Read `<meta name="tier">`, `<meta name="effort">`, and `<meta name="skills">` on the active node.
   - Inspect `rules/branches/meta/model-router-policy.html` only if you need provider-specific model mappings or escalation tie-breaking.
   - Load ONLY the recommended skill(s) listed in `<meta name="skills">`.
5. **Effort Scaling vs. Model Switch Check**:
   - Distinguish **raise_effort** (same model + higher effort when an automated verifier exists or mild ambiguity occurs) vs. **switch_model_up** (upgrade model tier when hitting the Reasoning Floor, Modal Ceiling without verifier, `>=2` failures, `>=4` coupled files, concurrency, or security) vs. **ground_before_think** (prefer retrieval/re-ranking over internal thinking tokens in RAG/lookup).
