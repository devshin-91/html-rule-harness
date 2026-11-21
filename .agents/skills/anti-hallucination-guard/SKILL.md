---
name: anti-hallucination-guard
description: Tier 3 verifier skill enforcing tool-first fact verification, quote-first line citations, premise checks, execution-backed validation, 5-lineage Gemini model spec boundaries (Flash/Lite, Hydrogen, Neon, Argon, Carbon), and Tier 0-2 deterministic reference auditing. Use when verifying API/SDK specs, auditing claims/citations, preventing reverse hallucination, or checking Gemini 4 Carbon/Argon/Hydrogen constraints.
---

# Anti-Hallucination Guard (Tier 3 Verifier)

## 1. Four Core Anti-Hallucination Principles
1. **Tool-First Verification & Zero Reverse Hallucination:** Never assert model IDs, SDK signatures, pricing, or language-version behavior from parametric memory, and never dismiss newer model generations as fictional. Verify in strict order:
   - Local code, config, and full operational logs (avoid lost-in-the-middle skips)
   - Official documentation skills/references and documentation servers
   - Web search and direct runtime execution
2. **Quote-First & Line Citations:** Quote the exact verbatim passage or code block before stating a conclusion, citing relative file paths and `#Lstart-Lend` line ranges verified directly on disk.
3. **Permission to Abstain & Premise Check:** If a quota, timeout, parameter, or citation is absent from observed sources, explicitly state that it cannot be confirmed rather than interpolating. Reject false premises, fabricated theorems, or unsupported API requests with counterexamples or official specs.
4. **Execute Before Claiming Done:** Never mentally compute hashes, dates, IEEE-754 floating-point rounding, encodings, async closure bindings, or bug patches. Run tests and verify actual outputs before reporting completion (use `Decimal(str(x))` + `ROUND_HALF_UP` for exact decimal arithmetic).

## 2. Five-Lineage Spec & Failure-Mode Guardrails
- **Flash/Lite (`gemini-3.5-flash-lite`, `gemini-3.8-flash`):** Prevent parametric overconfidence and reverse hallucination; drop removed sampling params (`temperature`, `top_p`, `top_k`); use `thinking_level >= medium` for multi-step cross-checks.
- **Hydrogen (`gemini-4-hydrogen`):** Prevent premature completion and missed hotfix overrides; `thinking_level` supports `low`, `medium`, `high` (default), `xhigh` (`minimal` and explicit caching `cachedContents`/`caches.create` unsupported).
- **Neon/Pro (`gemini-4-neon`):** Never mix deprecated legacy models into active rosters; preserve required discriminator fields (e.g., `"type": "antigravity"` in `agent_config`); test mathematical claims with counterexamples first.
- **Argon (`gemini-4-argon`):** Prevent over-rationalization (inventing undocumented SDK parameters); `thinking_level` supports `low`, `medium` (default), `high` (`xhigh`, `minimal`, explicit caching, and pixel-level image segmentation masks unsupported).
- **Carbon (`gemini-4-carbon`):** Prevent confident fabrication and partial "ghost completion" patches; shares Argon's `thinking_level` (`low`, `medium` default, `high`; no `xhigh`/`minimal`) and unsupported API boundaries; for **Long Decode**, require BOTH `background=True` AND `max_output_tokens > 65536`, join all `model_output` steps in `interaction.steps`, set HTTP read timeout >= 15-20 min, and **never use `total_input_tokens` for context compaction** (it sums across continuation hops).

## 3. Forward-Compatibility & Tier 0-2 Verification Pipeline
- **Forward-Compatibility:** Treat baseline model IDs as a floor; newer official releases and live official specs override baseline numbers; re-verify line ranges on disk before citing.
- **Tier 0 (Deterministic Local):** Validate `#Lstart-Lend` bounds, 1:1 in-text citation-to-reference mapping, and reference ordering offline.
- **Tier 1 (Cached Metadata):** Resolve DOIs/metadata via local cache before external lookup (zero LLM token spend for clean hits).
- **Tier 2 (Evidence Slicing):** Extract targeted source snippets with full-source cascade fallback when values span chunk boundaries; keep retries bounded (`max_continuations=2`) and require human final sign-off for high-stakes decisions.
