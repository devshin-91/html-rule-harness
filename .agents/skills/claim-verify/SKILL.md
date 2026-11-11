---
name: claim-verify
description: Low-to-mid complexity workflow for structured logical argument generation, concise synthesis, and strict claim-to-source verification. Use when generating short arguments, summarizing documents, or auditing references.
---

# Claim Verify & Structured Argument Workflow

## When Active
- Low-tier (`tier: low`, `effort: low`) for concise, single-source logical arguments or summaries.
- Mid-tier (`tier: mid`, `effort: medium`) when cross-checking multiple sources (`reference/`).

## Steps
1. Separate **Claims**, **Observed Evidence**, and **Assumptions/Inferences**.
2. Keep arguments tight: Premise -> Evidence -> Conclusion -> Counter-condition (if any).
3. Never state file paths, symbol names, metrics, or citations from memory—verify directly against observed files or tool output.
4. Escalate to `tier: mid` / `effort: medium` if conflicting sources or >3 dependencies appear.
