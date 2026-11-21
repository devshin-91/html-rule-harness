#!/usr/bin/env python3
"""Deterministic Markdown-to-HTML compiler and tree-data.js generator for Harness² rules.

Single source of truth: rules/src/router.md and rules/src/branches/<domain>/*.md
Compiled human/AI artifacts:
  - rules/router.html
  - rules/branches/<domain>/*.html
  - rules/assets/tree-data.js

Usage:
  python scripts/build_rules_html.py           # compile all MD sources -> HTML + tree-data.js
  python scripts/build_rules_html.py --check   # exit non-zero if any output is missing or out of sync
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

NODE_AI_BYTES_MAX = 2_800
VALID_TIERS = {"low", "mid", "high"}
VALID_EFFORTS = {"low", "medium", "high"}

_INLINE_TOKEN_RE = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*)")
_ORDERED_ITEM_RE = re.compile(r"^\d+\.\s+(.*)$")


@dataclass
class MdChildLink:
    """Outgoing conditional branch link parsed from a Markdown Branches table."""

    href: str
    target: str
    tier: str
    when: str
    label: str
    subtitle: str = ""

    @property
    def combined_label(self) -> str:
        """Exact label string matching _RuleHTMLParser extraction from <a>...</a>."""
        if self.subtitle:
            return " ".join(f"{self.label} {self.subtitle}".split())
        return " ".join(self.label.split())


@dataclass
class MdRuleDoc:
    """Structured rule node parsed from rules/src/**/*.md."""

    rule_id: str
    parent: str
    depth: int
    title: str
    html_title: str
    heading: str
    tier: str
    effort: str
    skills: list[str]
    pillars: list[str]
    keywords: list[str]
    escalate_when: list[str]
    src_rel_path: str
    html_rel_path: str
    escalation_policy: str = ""
    workload: str = ""
    nav_aria: str = ""
    summary_md: str = ""
    rules_heading: str = "적용 규칙"
    rules_ordered: bool = False
    rules_md: list[str] = field(default_factory=list)
    escalation_heading: str = "에스컬레이션 기준"
    escalation_md: list[str] = field(default_factory=list)
    branches_heading: str = "세부 분기"
    children: list[MdChildLink] = field(default_factory=list)
    human_ref_heading: str = ""
    human_ref_lines: list[str] = field(default_factory=list)
    md_bytes: int = 0

    @property
    def summary_plain(self) -> str:
        return " ".join(md_inline_to_plain(self.summary_md).split())

    @property
    def rules_plain(self) -> list[str]:
        return [" ".join(md_inline_to_plain(r).split()) for r in self.rules_md]

    @property
    def escalation_plain(self) -> str:
        parts = [" ".join(md_inline_to_plain(p).split()) for p in self.escalation_md if p.strip()]
        return " ".join(parts).strip()


def md_inline_to_html(text: str) -> str:
    """Convert inline Markdown (`code`, **bold**) to safe HTML without double-escaping."""
    out: list[str] = []
    pos = 0
    for m in _INLINE_TOKEN_RE.finditer(text):
        if m.start() > pos:
            out.append(html.escape(text[pos : m.start()], quote=False))
        tok = m.group(0)
        if tok.startswith("`") and tok.endswith("`"):
            out.append(f"<code>{html.escape(tok[1:-1], quote=False)}</code>")
        elif tok.startswith("**") and tok.endswith("**"):
            inner = md_inline_to_html(tok[2:-2])
            out.append(f"<strong>{inner}</strong>")
        pos = m.end()
    if pos < len(text):
        out.append(html.escape(text[pos:], quote=False))
    return "".join(out)


def md_inline_to_plain(text: str) -> str:
    """Strip inline Markdown (`code`, **bold**) to plain text matching HTML text extraction."""
    out: list[str] = []
    pos = 0
    for m in _INLINE_TOKEN_RE.finditer(text):
        if m.start() > pos:
            out.append(text[pos : m.start()])
        tok = m.group(0)
        if tok.startswith("`") and tok.endswith("`"):
            out.append(tok[1:-1])
        elif tok.startswith("**") and tok.endswith("**"):
            out.append(md_inline_to_plain(tok[2:-2]))
        pos = m.end()
    if pos < len(text):
        out.append(text[pos:])
    return "".join(out)


def _strip_quotes(val: str) -> str:
    s = val.strip()
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        inner = s[1:-1]
        if s[0] == '"':
            inner = inner.replace('\\"', '"').replace("\\\\", "\\")
        return inner
    return s


def _parse_inline_list(val: str) -> list[str]:
    inner = val.strip()[1:-1].strip()
    if not inner:
        return []
    items: list[str] = []
    buf: list[str] = []
    in_quote: str | None = None
    escape = False
    for ch in inner:
        if escape:
            buf.append(ch)
            escape = False
            continue
        if ch == "\\" and in_quote == '"':
            buf.append(ch)
            escape = True
            continue
        if in_quote:
            buf.append(ch)
            if ch == in_quote:
                in_quote = None
            continue
        if ch in ('"', "'"):
            in_quote = ch
            buf.append(ch)
        elif ch == ",":
            item = _strip_quotes("".join(buf))
            if item:
                items.append(item)
            buf = []
        else:
            buf.append(ch)
    tail = _strip_quotes("".join(buf))
    if tail:
        items.append(tail)
    return items


def parse_frontmatter(raw: str) -> tuple[dict[str, object], str]:
    """Parse minimal YAML frontmatter (scalars, inline lists, block lists) using stdlib only."""
    norm = raw.replace("\r\n", "\n")
    if not norm.startswith("---\n"):
        raise ValueError("Markdown rule file must start with YAML frontmatter '---'")
    end_idx = norm.find("\n---\n", 4)
    if end_idx == -1:
        if norm.endswith("\n---"):
            end_idx = len(norm) - 4
            body = ""
        else:
            raise ValueError("Unterminated YAML frontmatter block")
    else:
        body = norm[end_idx + 5 :]

    fm_lines = norm[4:end_idx].splitlines()
    data: dict[str, object] = {}
    current_list_key: str | None = None

    for line in fm_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and current_list_key is not None:
            lst = data[current_list_key]
            assert isinstance(lst, list)
            item = _strip_quotes(stripped[2:])
            if item:
                lst.append(item)
            continue
        current_list_key = None
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line!r}")
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val == "":
            data[key] = []
            current_list_key = key
        elif val.startswith("[") and val.endswith("]"):
            data[key] = _parse_inline_list(val)
        elif re.fullmatch(r"-?\d+", val):
            data[key] = int(val)
        else:
            data[key] = _strip_quotes(val)
    return data, body


def _split_md_table_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells: list[str] = []
    buf: list[str] = []
    escape = False
    for ch in s:
        if escape:
            buf.append(ch)
            escape = False
        elif ch == "\\":
            escape = True
        elif ch == "|":
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def _as_str_list(val: object, *, lower: bool = False) -> list[str]:
    if val is None or val == "":
        return []
    if isinstance(val, list):
        items = [str(x).strip() for x in val if str(x).strip()]
    else:
        items = [x.strip() for x in str(val).split(",") if x.strip()]
    if lower:
        items = [x.lower() for x in items]
    return items


def parse_md_rule_file(path: Path, src_root: Path) -> MdRuleDoc:
    """Parse one Markdown rule file in rules/src/ into an MdRuleDoc."""
    raw = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)

    rule_id = str(fm.get("rule_id", "")).strip()
    if not rule_id:
        raise ValueError(f"{path} missing frontmatter 'rule_id'")

    parent_raw = fm.get("parent", "")
    parent = "" if parent_raw in ("", [], None) else str(parent_raw).strip()
    depth = int(fm.get("depth", 0))
    title = str(fm.get("title", rule_id)).strip()
    html_title = str(fm.get("html_title", f"{title} · HTML Branching Rules")).strip()
    heading = str(fm.get("heading", title)).strip()
    tier = str(fm.get("tier", "mid")).strip()
    effort = str(fm.get("effort", "medium")).strip()
    skills = _as_str_list(fm.get("skills", []))
    pillars = _as_str_list(fm.get("pillars", []), lower=True)
    keywords = _as_str_list(fm.get("keywords", []), lower=True)
    escalate_when = [
        e for e in _as_str_list(fm.get("escalate_when", [])) if e.lower() != "none"
    ]
    escalation_policy = str(fm.get("escalation_policy", "")).strip()
    workload = str(fm.get("workload_profile", fm.get("workload", ""))).strip()
    nav_aria = str(fm.get("nav_aria", "")).strip()

    rel_from_src = path.relative_to(src_root).as_posix()
    src_rel_path = f"src/{rel_from_src}"
    html_rel_path = re.sub(r"\.md$", ".html", rel_from_src)

    # Split body into preamble (summary) and ## sections
    preamble_lines: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    cur_header: str | None = None
    cur_lines: list[str] = []

    for line in body.splitlines():
        if line.startswith("## "):
            if cur_header is not None:
                sections.append((cur_header, cur_lines))
            cur_header = line[3:].strip()
            cur_lines = []
        else:
            if cur_header is None:
                preamble_lines.append(line)
            else:
                cur_lines.append(line)
    if cur_header is not None:
        sections.append((cur_header, cur_lines))

    # Extract summary from preamble blockquote or first non-empty lines
    summary_parts: list[str] = []
    for line in preamble_lines:
        s = line.strip()
        if not s or s.startswith("# "):
            continue
        if s.startswith(">"):
            s = s[1:].strip()
        if s:
            summary_parts.append(s)
    summary_md = " ".join(summary_parts).strip()

    rules_heading = "적용 규칙"
    rules_ordered = False
    rules_md: list[str] = []
    escalation_heading = "에스컬레이션 기준"
    escalation_md: list[str] = []
    branches_heading = "세부 분기"
    children: list[MdChildLink] = []
    human_ref_heading = ""
    human_ref_lines: list[str] = []

    for header, lines in sections:
        h_lower = header.lower()
        if h_lower == "rules" or h_lower.startswith("rules:"):
            if ":" in header:
                rules_heading = header.split(":", 1)[1].strip() or rules_heading
            for ln in lines:
                s = ln.strip()
                if not s:
                    continue
                if s.startswith("- ") or s.startswith("* "):
                    rules_md.append(s[2:].strip())
                elif m := _ORDERED_ITEM_RE.match(s):
                    rules_ordered = True
                    rules_md.append(m.group(1).strip())
        elif h_lower == "escalation" or h_lower.startswith("escalation:"):
            if ":" in header:
                escalation_heading = header.split(":", 1)[1].strip() or escalation_heading
            for ln in lines:
                s = ln.strip()
                if not s:
                    continue
                if s.startswith("- ") or s.startswith("* "):
                    s = s[2:].strip()
                escalation_md.append(s)
        elif h_lower == "branches" or h_lower.startswith("branches:"):
            if ":" in header:
                branches_heading = header.split(":", 1)[1].strip() or branches_heading
            table_lines = [ln.strip() for ln in lines if ln.strip().startswith("|")]
            if len(table_lines) >= 3:
                cols = [c.lower() for c in _split_md_table_row(table_lines[0])]
                for row_ln in table_lines[2:]:
                    vals = _split_md_table_row(row_ln)
                    row = {
                        cols[i]: (vals[i] if i < len(vals) else "")
                        for i in range(len(cols))
                    }
                    children.append(
                        MdChildLink(
                            target=md_inline_to_plain(row.get("target", "")).strip(),
                            href=md_inline_to_plain(row.get("href", "")).strip(),
                            tier=md_inline_to_plain(row.get("tier", "mid")).strip() or "mid",
                            label=row.get("label", "").strip(),
                            when=md_inline_to_plain(row.get("when", "")).strip(),
                            subtitle=row.get("subtitle", "").strip(),
                        )
                    )
        elif h_lower == "human reference" or h_lower.startswith("human reference:"):
            human_ref_heading = (
                header.split(":", 1)[1].strip() if ":" in header else "Human Reference"
            )
            human_ref_lines = [ln for ln in lines]

    return MdRuleDoc(
        rule_id=rule_id,
        parent=parent,
        depth=depth,
        title=title,
        html_title=html_title,
        heading=heading,
        tier=tier,
        effort=effort,
        skills=skills,
        pillars=pillars,
        keywords=keywords,
        escalate_when=escalate_when,
        src_rel_path=src_rel_path,
        html_rel_path=html_rel_path,
        escalation_policy=escalation_policy,
        workload=workload,
        nav_aria=nav_aria or branches_heading,
        summary_md=summary_md,
        rules_heading=rules_heading,
        rules_ordered=rules_ordered,
        rules_md=rules_md,
        escalation_heading=escalation_heading,
        escalation_md=escalation_md,
        branches_heading=branches_heading,
        children=children,
        human_ref_heading=human_ref_heading,
        human_ref_lines=human_ref_lines,
        md_bytes=len(raw.encode("utf-8")),
    )


def load_md_tree(src_root: Path) -> dict[str, MdRuleDoc]:
    """Load rules/src/router.md and rules/src/branches/**/*.md in deterministic order."""
    files = [src_root / "router.md", *sorted((src_root / "branches").rglob("*.md"))]
    docs: dict[str, MdRuleDoc] = {}
    for f in files:
        if not f.is_file():
            continue
        doc = parse_md_rule_file(f, src_root)
        if doc.rule_id in docs:
            raise ValueError(f"Duplicate rule_id {doc.rule_id!r} in {f}")
        docs[doc.rule_id] = doc
    return docs


def _render_human_reference_section(heading: str, lines: list[str]) -> str:
    """Render optional Human Reference Markdown (tables/lists/paragraphs) outside AI-RULE block."""
    body_parts: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i].strip()
        if not ln:
            i += 1
            continue
        if ln.startswith("|") and i + 1 < n and lines[i + 1].strip().startswith("|"):
            headers = _split_md_table_row(ln)
            i += 2  # skip header + separator
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_md_table_row(lines[i]))
                i += 1
            th_html = "".join(f"<th>{md_inline_to_html(h)}</th>" for h in headers)
            tr_html = "\n".join(
                "        <tr>"
                + "".join(f"<td>{md_inline_to_html(c)}</td>" for c in r)
                + "</tr>"
                for r in rows
            )
            body_parts.append(
                "    <table class=\"policy-table\">\n"
                "      <thead>\n"
                f"        <tr>{th_html}</tr>\n"
                "      </thead>\n"
                "      <tbody>\n"
                f"{tr_html}\n"
                "      </tbody>\n"
                "    </table>"
            )
        elif ln.startswith("- ") or ln.startswith("* "):
            items: list[str] = []
            while i < n and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            li_html = "\n".join(f"      <li>{md_inline_to_html(it)}</li>" for it in items)
            body_parts.append(f"    <ul>\n{li_html}\n    </ul>")
        else:
            body_parts.append(f"    <p>{md_inline_to_html(ln)}</p>")
            i += 1

    inner = "\n".join(body_parts)
    return (
        "\n<section class=\"rule-node\" style=\"margin-top:0;\">\n"
        "  <div class=\"rule-card\">\n"
        f"    <h2>{html.escape(heading, quote=False)}</h2>\n"
        f"{inner}\n"
        "  </div>\n"
        "</section>"
    )


def render_rule_html(doc: MdRuleDoc) -> str:
    """Deterministically compile an MdRuleDoc into semantic HTML with AI-RULE markers."""
    dir_depth = len(Path(doc.html_rel_path).parent.parts)
    asset_prefix = "../" * dir_depth

    attrs: list[tuple[str, str]] = [
        ("class", "rule-node"),
        ("data-rule-id", doc.rule_id),
        ("data-parent", doc.parent),
        ("data-depth", str(doc.depth)),
        ("data-title", doc.title),
        ("data-tier", doc.tier),
        ("data-effort", doc.effort),
        ("data-skills", ",".join(doc.skills)),
    ]
    if doc.pillars:
        attrs.append(("data-pillars", ",".join(doc.pillars)))
    attrs.append(("data-keywords", ",".join(doc.keywords)))
    if doc.escalation_policy:
        attrs.append(("data-escalation-policy", doc.escalation_policy))
    if doc.workload:
        attrs.append(("data-workload", doc.workload))
    attrs.append(
        ("data-escalate-when", "|".join(doc.escalate_when) if doc.escalate_when else "none")
    )

    main_open_lines = [f'<main {attrs[0][0]}="{html.escape(attrs[0][1], quote=True)}"']
    for idx, (k, v) in enumerate(attrs[1:], start=1):
        end_ch = ">" if idx == len(attrs) - 1 else ""
        main_open_lines.append(f'      {k}="{html.escape(v, quote=True)}"{end_ch}')
    main_open = "\n".join(main_open_lines)

    sections_html: list[str] = []
    sections_html.append(
        "  <header class=\"rule-head\">\n"
        f"    <h1>{html.escape(doc.heading, quote=False)}</h1>\n"
        f"    <p class=\"rule-summary\">{md_inline_to_html(doc.summary_md)}</p>\n"
        "  </header>"
    )

    if doc.rules_md:
        list_tag = "ol" if doc.rules_ordered else "ul"
        li_lines = "\n".join(f"      <li>{md_inline_to_html(r)}</li>" for r in doc.rules_md)
        sections_html.append(
            "  <section class=\"rule-card\" data-rules>\n"
            f"    <h2>{html.escape(doc.rules_heading, quote=False)}</h2>\n"
            f"    <{list_tag}>\n"
            f"{li_lines}\n"
            f"    </{list_tag}>\n"
            "  </section>"
        )

    if doc.escalation_md:
        p_lines = "\n".join(f"    <p>{md_inline_to_html(p)}</p>" for p in doc.escalation_md)
        sections_html.append(
            "  <section class=\"rule-card alert-escalate\" data-escalation>\n"
            f"    <h2>{html.escape(doc.escalation_heading, quote=False)}</h2>\n"
            f"{p_lines}\n"
            "  </section>"
        )

    if doc.children:
        link_lines: list[str] = []
        for ch in doc.children:
            href_e = html.escape(ch.href, quote=True)
            tgt_e = html.escape(ch.target, quote=True)
            tier_e = html.escape(ch.tier, quote=True)
            when_e = html.escape(ch.when, quote=True)
            label_h = md_inline_to_html(ch.label)
            if ch.subtitle:
                sub_h = md_inline_to_html(ch.subtitle)
                link_lines.append(
                    f'    <a class="branch-link" href="{href_e}" data-target="{tgt_e}" '
                    f'data-tier="{tier_e}" data-when="{when_e}">'
                    f"<strong>{label_h}</strong> <span>{sub_h}</span></a>"
                )
            else:
                link_lines.append(
                    f'    <a class="branch-link" href="{href_e}" data-target="{tgt_e}" '
                    f'data-tier="{tier_e}" data-when="{when_e}">'
                    f"<strong>{label_h}</strong></a>"
                )
        aria_e = html.escape(doc.nav_aria, quote=True)
        links_block = "\n".join(link_lines)
        sections_html.append(
            f'  <nav class="branch-grid" data-children aria-label="{aria_e}">\n'
            f"    <h2>{html.escape(doc.branches_heading, quote=False)}</h2>\n"
            f"{links_block}\n"
            "  </nav>"
        )

    ai_body = f"{main_open}\n" + "\n\n".join(sections_html) + "\n</main>"
    human_ref_html = (
        _render_human_reference_section(doc.human_ref_heading, doc.human_ref_lines)
        if doc.human_ref_heading and doc.human_ref_lines
        else ""
    )

    return (
        "<!doctype html>\n"
        "<html lang=\"ko\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"  <title>{html.escape(doc.html_title, quote=False)}</title>\n"
        f'  <link rel="stylesheet" href="{asset_prefix}assets/rule-ui.css">\n'
        "</head>\n"
        "<body>\n"
        f"<!-- Compiled from rules/{doc.src_rel_path} by scripts/build_rules_html.py — edit Markdown source, not HTML -->\n"
        "<!-- AI-RULE-START -->\n"
        f"{ai_body}\n"
        "<!-- AI-RULE-END -->"
        f"{human_ref_html}\n"
        f'<script src="{asset_prefix}assets/rule-ui.js" defer></script>\n'
        "</body>\n"
        "</html>\n"
    )


def _extract_ai_bytes(raw_html: str) -> int:
    start_marker = "<!-- AI-RULE-START -->"
    end_marker = "<!-- AI-RULE-END -->"
    start = raw_html.index(start_marker) + len(start_marker)
    end = raw_html.index(end_marker)
    return len(raw_html[start:end].strip().encode("utf-8"))


def _read_skill_descriptions(root: Path) -> dict[str, str]:
    skills_dir = root / ".agents" / "skills"
    meta: dict[str, str] = {}
    if not skills_dir.is_dir():
        return meta
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        raw = skill_md.read_text(encoding="utf-8")[:1200]
        m_desc = re.search(r"^description:\s*(.+)$", raw, re.M)
        meta[skill_md.parent.name] = m_desc.group(1).strip() if m_desc else ""
    return meta


def render_tree_data_js(
    root: Path,
    docs: dict[str, MdRuleDoc],
    rendered_html: dict[str, str],
) -> str:
    """Emit deterministic rules/assets/tree-data.js for zero-CORS Explorer rendering."""
    rules_root = root / "rules"
    cat_path = rules_root / "model-catalog.json"
    h_path = rules_root / "skill-hierarchy.json"
    catalog = json.loads(cat_path.read_text(encoding="utf-8")) if cat_path.is_file() else {}
    hierarchy = json.loads(h_path.read_text(encoding="utf-8")) if h_path.is_file() else {}
    skill_meta = _read_skill_descriptions(root)

    nodes_payload: dict[str, dict] = {}
    for nid, doc in docs.items():
        html_text = rendered_html[nid]
        nodes_payload[nid] = {
            "rule_id": doc.rule_id,
            "parent": doc.parent,
            "depth": doc.depth,
            "title": doc.title,
            "tier": doc.tier,
            "effort": doc.effort,
            "skills": doc.skills,
            "pillars": doc.pillars,
            "keywords": doc.keywords,
            "escalate_when": doc.escalate_when,
            "escalation_policy": doc.escalation_policy,
            "workload": doc.workload,
            "rel_path": doc.html_rel_path,
            "src_path": doc.src_rel_path,
            "summary": doc.summary_plain,
            "rules": doc.rules_plain,
            "escalation_note": doc.escalation_plain,
            "ai_bytes": _extract_ai_bytes(html_text),
            "file_bytes": len(html_text.encode("utf-8")),
            "md_bytes": doc.md_bytes,
            "children": [
                {
                    "href": ch.href,
                    "target": ch.target,
                    "tier": ch.tier,
                    "when": ch.when,
                    "label": ch.combined_label,
                }
                for ch in doc.children
            ],
        }

    payload = {
        "generated_by": "scripts/build_rules_html.py",
        "source_of_truth": "rules/src/**/*.md",
        "skills": skill_meta,
        "skill_hierarchy": hierarchy,
        "catalog": catalog,
        "nodes": nodes_payload,
    }
    return (
        "// Auto-generated by scripts/build_rules_html.py from rules/src/**/*.md — do not hand-edit.\n"
        f"window.RULE_TREE_DATA = {json.dumps(payload, ensure_ascii=False, indent=2)};\n"
    )


def compile_rules(root: Path, *, check: bool = False) -> tuple[bool, list[str], dict]:
    """Compile rules/src/**/*.md -> HTML + tree-data.js, or verify sync in --check mode."""
    rules_root = root / "rules"
    src_root = rules_root / "src"
    issues: list[str] = []

    if not (src_root / "router.md").is_file():
        return False, ["missing rules/src/router.md"], {}

    docs = load_md_tree(src_root)
    rendered_html: dict[str, str] = {}
    expected_outputs: dict[Path, str] = {}

    for nid, doc in docs.items():
        if doc.tier not in VALID_TIERS:
            issues.append(f"{doc.src_rel_path}: invalid tier {doc.tier!r}")
        if doc.effort not in VALID_EFFORTS:
            issues.append(f"{doc.src_rel_path}: invalid effort {doc.effort!r}")
        html_text = render_rule_html(doc)
        ai_bytes = _extract_ai_bytes(html_text)
        if ai_bytes > NODE_AI_BYTES_MAX:
            issues.append(
                f"{doc.html_rel_path}: compiled AI block is {ai_bytes}B (> {NODE_AI_BYTES_MAX}B cap)"
            )
        rendered_html[nid] = html_text
        expected_outputs[rules_root / doc.html_rel_path] = html_text

    tree_js_path = rules_root / "assets" / "tree-data.js"
    expected_outputs[tree_js_path] = render_tree_data_js(root, docs, rendered_html)

    # Detect stale HTML files in rules/branches/ that no longer have an MD source
    expected_branch_html = {
        p.resolve() for p in expected_outputs if p.suffix == ".html" and "branches" in p.parts
    }
    branches_dir = rules_root / "branches"
    if branches_dir.is_dir():
        for existing_html in sorted(branches_dir.rglob("*.html")):
            if existing_html.resolve() not in expected_branch_html:
                issues.append(
                    f"stale compiled HTML without MD source: {existing_html.relative_to(root).as_posix()}"
                )

    changed = 0
    for out_path, expected_content in expected_outputs.items():
        current = out_path.read_text(encoding="utf-8") if out_path.is_file() else None
        if current != expected_content:
            if check:
                issues.append(
                    f"out of sync with MD source: {out_path.relative_to(root).as_posix()}"
                )
            else:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                with out_path.open("w", encoding="utf-8", newline="\n") as fh:
                    fh.write(expected_content)
                changed += 1

    total_md_bytes = sum(d.md_bytes for d in docs.values())
    total_ai_bytes = sum(_extract_ai_bytes(rendered_html[nid]) for nid in docs)
    total_html_bytes = sum(len(rendered_html[nid].encode("utf-8")) for nid in docs)
    summary = {
        "md_nodes": len(docs),
        "html_nodes": len(rendered_html),
        "total_md_bytes": total_md_bytes,
        "total_ai_bytes": total_ai_bytes,
        "total_html_bytes": total_html_bytes,
        "max_node_ai_bytes": max((_extract_ai_bytes(h) for h in rendered_html.values()), default=0),
        "files_written": changed,
        "mode": "check" if check else "build",
    }
    return len(issues) == 0, issues, summary


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compile rules/src/**/*.md into HTML branch views and rules/assets/tree-data.js."
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root directory.",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Verify compiled HTML and tree-data.js match Markdown sources without writing.",
    )
    args = ap.parse_args()

    ok, issues, summary = compile_rules(args.root, check=args.check)
    for item in issues:
        print(f"[ERROR] {item}", file=sys.stderr)
    print(f"[BUILD-SUMMARY] {json.dumps(summary, ensure_ascii=False)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
