---
name: architecture-rfc
description: High-tier engineering workflow for multi-module design, concurrency/distributed debugging, migrations, and trade-off analysis. Use for complex system design or escalated high-risk tasks.
---

# Architecture RFC & High-Complexity Workflow

## Recommended Profile
- Default: **High-tier model (`high`)**, **High reasoning effort (`high`)**.

## Steps
1. **Boundary & Invariant Map**: Identify all affected modules, data contracts, state transitions, and failure modes before editing.
2. **Option Matrix**: Compare at least 2 concrete designs across context cost, latency, maintainability, and failure recovery; record major decisions in `tradeoff.md` if persistent.
3. **Incremental Execution**: Implement behind clear boundaries with deterministic validation scripts/tests at each step.
4. **Adversarial Verification**: Check edge cases, error paths, concurrency/race risks, and schema invariants before completion.
