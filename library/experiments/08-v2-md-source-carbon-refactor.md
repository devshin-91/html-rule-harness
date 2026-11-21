# Iteration 08 — v2.0 MD-Source → HTML-Compiled Refactor, Anti-Hallucination Guardrails & Gemini 4 v3.0 Catalog

## Goal
Refactor `html-rule-harness` to **v2.0** by integrating three verified architectural pillars without breaking backward compatibility or Harness² context budgets:
1. **MD Single Source of Truth → Deterministic HTML Views (`md-html-guide`)**: Author all rules as concise Markdown with YAML frontmatter (`rules/src/**/*.md`), deterministically compile human HTML views + `tree-data.js` at 0 LLM tokens (`scripts/build_rules_html.py`), parse MD primary in `scripts/resolve_rule.py`, and close the Explorer UI review loop with **JSON** & **Markdown** Export buttons.
2. **5-Lineage Anti-Hallucination Guardrails (`antigravity-gemini-anti-hallucination`)**: Add dedicated branch `meta.anti-hallucination` (`rules/src/branches/meta/anti-hallucination.md`) and Tier 3 verifier skill `anti-hallucination-guard` enforcing tool-first verification, quote-first `#Lstart-Lend` citations, premise checking, execution-backed validation, and Tier 0–2 deterministic fact checking.
3. **Verified Gemini 4 / 3.5 / Decisions API Catalog (`model-catalog.json` v3.0)**: Upgrade the active model catalog to `gemini-3.5-flash-lite`, `gemini-3.8-flash`, `gemini-decision-1` (`v1beta`), `gemini-4-hydrogen`, `gemini-4-neon`, `gemini-4-argon`, and `gemini-4-carbon` with exact `thinking_level` bounds, unsupported API boundaries, Long Decode requirements, and zero legacy 1.x/2.x models.

## Design (Propose–Probe–Compose)
- **Source & Compiler (`rules/src/**/*.md` + `scripts/build_rules_html.py`)**:
  - Losslessly converted all 27 existing HTML rule nodes to Markdown + YAML frontmatter and added 1 new node (`rules/src/branches/meta/anti-hallucination.md`) for **28 total nodes**.
  - Implemented stdlib-only deterministic compiler `scripts/build_rules_html.py` with `--check` drift detection (fails non-zero if any compiled HTML or `rules/assets/tree-data.js` diverges from `rules/src/**/*.md`).
- **Router, Validator & Tests (`scripts/resolve_rule.py`, `scripts/validate_harness.py`, `tests/test_rules_harness.py`)**:
  - Updated `resolve_rule.py` to read `rules/src/**/*.md` as primary source with automatic HTML fallback (`stats.source_format: "md"|"html"`, `--source {auto,md,html}`).
  - Updated `validate_harness.py` to verify MD-to-HTML sync (`compile_rules(root, check=True)`), 28 MD/HTML node parity, 9 skills, active v3.0 catalog constraints, and `AGENTS.md <= 8,000` chars.
  - Expanded unit test suite from 12 to **17 tests** covering MD-primary routing, HTML fallback, full 28-node MD-vs-HTML parity, `--check` drift detection, `meta.anti-hallucination` pipeline routing, and v3.0 Gemini 4 spec bounds.
- **Explorer UI v2.0 & Governance Docs (`rules/index.html`, `rules/assets/rule-ui.{js,css}`, `AGENTS.md`, `README.md`)**:
  - Added `MD Source → HTML View` provenance pill & notice banner, **`JSON 설정 내보내기`** (`rule-config-<branch>.json`) and **`Markdown 규칙 패킷 내보내기`** (`rule-packet-<branch>.md`) downloads alongside XML copy, **`환각 검증 [Anti-Hallucination]`** preset, Markdown source custom builder, and v3.0 catalog fallback while preserving Warm Stone Paper (`#F6F5F0`) / Forest Teal (`#0F766E`) zero-slop styling and commercially-free stock credits.
  - Added `anti-hallucination-guard` trigger and MD-source architecture invariants to `AGENTS.md` (`5,395 / 8,000 chars`).

## Verification & Observed Metrics
- **`python scripts/build_rules_html.py --check`**: exit `0`
  - `md_nodes`: `28`, `html_nodes`: `28`, `files_written`: `0` (`mode: "check"`)
  - `total_md_bytes`: `45,916 B` vs `total_html_bytes`: `73,564 B` (`total_ai_bytes`: `54,210 B`, `max_node_ai_bytes`: `2,764 B <= 2,800 B`)
- **`python scripts/validate_harness.py`**: exit `0`
  - `always_on_chars`: `5,395 / 8,000`, `skills`: `9`, `md_html_in_sync`: `true`, `model_catalog_version`: `"3.0"`
- **`python scripts/scan_skills_security.py`**: exit `0`
  - `scanned_skills`: `9`, `findings`: `[]`, `blocking_count`: `0`, `passed`: `true`
- **`python -m unittest discover -s tests -v`**: exit `0` (`Ran 17 tests`, `OK`)
- **`node --check rules/assets/rule-ui.js`**: exit `0`
- **Live Route Probe (`"Gemini 4 Carbon 환각 검증 및 근거 인용 감사"`)**:
  - `source_format`: `"md"`, chain: `root -> meta.root -> meta.anti-hallucination`
  - `tier`: `"high"`, `effort`: `"high"`, `skill_pipeline`: `architecture-rfc -> claim-verify -> anti-hallucination-guard`, `saved_pct`: `94.0%`

## Key Lessons
1. Keeping Markdown (`rules/src/**/*.md`) as the single source of truth and compiling HTML views deterministically eliminates hand-edit drift and avoids feeding verbose HTML back to AI agents while preserving rich human visual review.
2. Providing native `.json` and `.md` export buttons closes the interactive review loop (`md-html-guide`) so simulator decisions flow cleanly into agent prompts or source edits.
3. Encoding exact per-model boundaries (`gemini-4-carbon`/`argon` no `xhigh`/`minimal`/explicit caching/pixel masks; `gemini-4-hydrogen` supports `xhigh` but not `minimal`/explicit caching; Long Decode requires both `background=True` and `max_output_tokens > 65536` without `total_input_tokens` compaction) directly inside `model-catalog.json` v3.0 and `meta.anti-hallucination` prevents both spec fabrication and reverse hallucination.
