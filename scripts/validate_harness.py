#!/usr/bin/env python3
"""Google Harness² surface validator and HTML tree-data generator."""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path

from resolve_rule import extract_ai_block, load_model_catalog, load_skill_hierarchy, load_tree
from scan_skills_security import scan_skills_root

ALWAYS_ON_MAX = 8_000
NODE_AI_BYTES_WARN = 1_500
NODE_AI_BYTES_MAX = 2_800
RECOMMENDED_MAX_DEPTH = 3
VALID_TIERS = {"low", "mid", "high"}
VALID_EFFORTS = {"low", "medium", "high"}
VALID_PILLARS = {"prompt", "context", "harness", "loop", "graph"}
VALID_POLICIES = {
    "effort-first-with-verifier",
    "capacity-switch-sensitive",
    "grounding-over-thinking",
    "overthinking-guard-low",
}
JINJA_TRAPS = re.compile(r"\{\{|\{%|\{#")


def _parse_skill_frontmatter(skill_md: Path) -> tuple[str, str]:
    raw = skill_md.read_text(encoding="utf-8")[:1000]
    m_desc = re.search(r"^description:\s*(.+)$", raw, re.M)
    m_name = re.search(r"^name:\s*(\S+)\s*$", raw, re.M)
    return (m_name.group(1) if m_name else "", m_desc.group(1).strip() if m_desc else "")


def validate_harness(root: Path) -> tuple[list[str], list[str], dict]:
    """Validate Harness² invariants and HTML rule tree consistency. Returns (errors, warnings, summary)."""
    errors: list[str] = []
    warnings: list[str] = []

    agents_md = root / "AGENTS.md"
    if not agents_md.is_file():
        errors.append("missing AGENTS.md")
        return errors, warnings, {}
    agents_text = agents_md.read_text(encoding="utf-8")
    if not agents_text.strip():
        errors.append("AGENTS.md must not be empty")
    if len(agents_text) > ALWAYS_ON_MAX:
        errors.append(f"AGENTS.md is {len(agents_text)} chars (> {ALWAYS_ON_MAX} cap)")
    if m := JINJA_TRAPS.search(agents_text):
        errors.append(f"AGENTS.md contains Jinja brace trap {m.group(0)!r}")

    # Validate .agents/skills/*/SKILL.md + trigger lines in AGENTS.md
    skills_dir = root / ".agents" / "skills"
    skill_meta: dict[str, str] = {}
    if skills_dir.is_dir():
        for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
            sdir = skill_md.parent.name
            fm_name, fm_desc = _parse_skill_frontmatter(skill_md)
            if not fm_desc:
                errors.append(f"{skill_md.relative_to(root)} missing YAML description:")
            if fm_name and fm_name != sdir:
                errors.append(f"{skill_md.relative_to(root)} name:{fm_name!r} != dir {sdir!r}")
            if sdir not in agents_text:
                errors.append(f"skill {sdir!r} is missing a verbatim trigger line in AGENTS.md")
            skill_meta[sdir] = fm_desc

    # Compile-check Python helpers in scripts/
    for py_file in sorted((root / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{py_file.relative_to(root)} compile error: {exc.msg}")

    # Security scan all skills & verify hierarchy registration
    sec_report = scan_skills_root(skills_dir)
    for f in sec_report["findings"]:
        if f["severity"] in {"CRITICAL", "HIGH"}:
            errors.append(
                f"security gate blocked {f['skill']}/{f['file']}:{f['line']} [{f['rule_id']}] {f['reason']}"
            )
        else:
            warnings.append(
                f"security warning {f['skill']}/{f['file']}:{f['line']} [{f['rule_id']}] {f['reason']}"
            )

    rules_root = root / "rules"
    hierarchy = load_skill_hierarchy(rules_root)
    h_skills = hierarchy.get("skills", {})
    for sk in skill_meta:
        if sk not in h_skills:
            errors.append(f"skill {sk!r} missing from rules/skill-hierarchy.json (flat/unranked skill prohibited)")

    # Validate HTML rule tree
    nodes = load_tree(rules_root)
    if "root" not in nodes:
        errors.append("rules/router.html must define data-rule-id='root'")

    for nid, node in nodes.items():
        html_path = rules_root / node.rel_path
        raw = html_path.read_text(encoding="utf-8")
        if "<!-- AI-RULE-START -->" not in raw or "<!-- AI-RULE-END -->" not in raw:
            errors.append(f"{node.rel_path} missing AI-RULE-START/END markers")
        ai_block = extract_ai_block(raw)
        if "<style" in ai_block.lower() or "<script" in ai_block.lower():
            errors.append(f"{node.rel_path} embeds inline <style> or <script> inside AI-RULE block")
        if node.tier not in VALID_TIERS:
            errors.append(f"{node.rel_path} invalid data-tier={node.tier!r}")
        if node.effort not in VALID_EFFORTS:
            errors.append(f"{node.rel_path} invalid data-effort={node.effort!r}")
        if node.parent and node.parent not in nodes:
            errors.append(f"{node.rel_path} missing parent {node.parent!r}")
        if node.ai_bytes > NODE_AI_BYTES_MAX:
            errors.append(f"{node.rel_path} AI block is {node.ai_bytes}B (> {NODE_AI_BYTES_MAX}B cap)")
        elif node.ai_bytes > NODE_AI_BYTES_WARN:
            warnings.append(f"{node.rel_path} AI block is {node.ai_bytes}B (above {NODE_AI_BYTES_WARN}B target)")
        if node.depth > RECOMMENDED_MAX_DEPTH:
            warnings.append(
                f"{node.rel_path} depth={node.depth} exceeds recommended depth {RECOMMENDED_MAX_DEPTH} (arXiv:2607.17598)"
            )

        for sk in node.skills:
            if sk not in skill_meta:
                errors.append(f"{node.rel_path} references unknown skill {sk!r}")
        for pl in node.pillars:
            if pl not in VALID_PILLARS:
                errors.append(f"{node.rel_path} invalid data-pillars value {pl!r}")
        if node.escalation_policy and node.escalation_policy not in VALID_POLICIES:
            errors.append(f"{node.rel_path} invalid data-escalation-policy {node.escalation_policy!r}")

        for link in node.children:
            if link.target not in nodes:
                errors.append(f"{node.rel_path} broken child target {link.target!r}")
                continue
            resolved_href = (html_path.parent / link.href).resolve()
            expected_file = (rules_root / nodes[link.target].rel_path).resolve()
            if resolved_href != expected_file:
                errors.append(
                    f"{node.rel_path} href {link.href!r} resolves to {resolved_href.name}, "
                    f"expected {expected_file.name}"
                )

    summary = {
        "always_on_chars": len(agents_text),
        "always_on_cap": ALWAYS_ON_MAX,
        "skills": len(skill_meta),
        "html_nodes": len(nodes),
        "total_ai_bytes": sum(n.ai_bytes for n in nodes.values()),
        "total_file_bytes": sum(n.file_bytes for n in nodes.values()),
    }
    if not errors:
        sync_tree_data_js(rules_root, nodes, skill_meta, hierarchy)
    return errors, warnings, summary


def sync_tree_data_js(rules_root: Path, nodes: dict, skill_meta: dict[str, str], hierarchy: dict) -> None:
    """Emit rules/assets/tree-data.js so rules/index.html works over file:// with zero CORS."""
    catalog = load_model_catalog(rules_root)
    payload = {
        "generated_by": "scripts/validate_harness.py",
        "skills": skill_meta,
        "skill_hierarchy": hierarchy,
        "catalog": catalog,
        "nodes": {
            nid: {
                "rule_id": n.rule_id,
                "parent": n.parent,
                "depth": n.depth,
                "title": n.title,
                "tier": n.tier,
                "effort": n.effort,
                "skills": n.skills,
                "pillars": n.pillars,
                "keywords": n.keywords,
                "escalate_when": n.escalate_when,
                "escalation_policy": n.escalation_policy,
                "workload": n.workload,
                "rel_path": n.rel_path,
                "summary": n.summary,
                "rules": n.rules,
                "escalation_note": n.escalation_note,
                "ai_bytes": n.ai_bytes,
                "file_bytes": n.file_bytes,
                "children": [
                    {
                        "href": c.href,
                        "target": c.target,
                        "tier": c.tier,
                        "when": c.when,
                        "label": c.label,
                    }
                    for c in n.children
                ],
            }
            for nid, n in nodes.items()
        },
    }
    out = rules_root / "assets" / "tree-data.js"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "// Auto-generated by scripts/validate_harness.py — do not hand-edit.\n"
        f"window.RULE_TREE_DATA = {json.dumps(payload, ensure_ascii=False, indent=2)};\n",
        encoding="utf-8",
    )


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors, warnings, summary = validate_harness(root)
    for w in warnings:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[ERROR] {e}", file=sys.stderr)
    print(f"[SUMMARY] {json.dumps(summary, ensure_ascii=False)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
