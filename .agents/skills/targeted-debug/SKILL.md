---
name: targeted-debug
description: Mid-tier engineering workflow for reproducing bugs, isolating root causes, writing minimal patches, and verifying fixes with targeted tests. Use for debugging, error investigation, or localized code modifications.
---

# Targeted Debug & Patch Workflow

## Recommended Profile
- Default: **Mid-tier model (`mid`)**, **Medium reasoning effort (`medium`)**.
- Escalate to **High-tier (`high`)** + `architecture-rfc` if root cause spans concurrency/async races, security boundaries, >3 coupled modules, or fails 2 consecutive patch attempts.

## Steps
1. **Reproduce First**: Run the minimal failing command or test to observe the exact error/stack trace.
2. **Locate Economically**: Search for the symbol/error string before reading files; read only the relevant function/block.
3. **Patch Minimally**: Fix the root cause cleanly without refactoring unrelated code.
4. **Verify**: Re-run the failing test/check plus surrounding checks after the final edit; report exact scope and results.
