#!/usr/bin/env python3
"""Minimal-context HTML branching rule resolver & difficulty/model tier explorer."""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

TIER_ORDER = {"low": 0, "mid": 1, "high": 2}
TIER_NAMES = ("low", "mid", "high")
EFFORT_BY_TIER = {"low": "low", "mid": "medium", "high": "high"}
TOKEN_PATTERN = re.compile(r"[a-z0-9가-힣_]+", re.I)
PILLAR_SIGNALS = {
    "prompt": ("prompt", "few-shot", "json schema", "pydantic", "dspy", "프롬프트", "스키마"),
    "context": ("context", "rag", "graphrag", "mem0", "memory", "compaction", "컨텍스트", "메모리", "검색"),
    "harness": ("harness", "sandbox", "hook", "guardrail", "eval", "하네스", "샌드박스", "훅", "가드레일", "테스트 게이트"),
    "loop": ("loop", "react", "reflexion", "evaluator-optimizer", "retry", "루프", "반복", "자가수정"),
    "graph": ("graph", "langgraph", "adk", "workflow", "multi-agent", "hitl", "그래프", "멀티에이전트", "상태 전이"),
}


@dataclass
class ChildLink:
    """Outgoing conditional branch link from an HTML rule node."""

    href: str
    target: str
    tier: str
    when: str
    label: str = ""


@dataclass
class RuleNode:
    """Parsed semantic rule payload extracted from <!-- AI-RULE-START/END -->."""

    rule_id: str
    parent: str
    depth: int
    title: str
    tier: str
    effort: str
    skills: list[str]
    pillars: list[str]
    keywords: list[str]
    escalate_when: list[str]
    rel_path: str
    escalation_policy: str = ""
    workload: str = ""
    summary: str = ""
    rules: list[str] = field(default_factory=list)
    escalation_note: str = ""
    children: list[ChildLink] = field(default_factory=list)
    ai_bytes: int = 0
    file_bytes: int = 0


class _RuleHTMLParser(HTMLParser):
    """Lightweight stdlib parser for semantic HTML rule nodes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.main_attrs: dict[str, str] = {}
        self.summary = ""
        self.rules: list[str] = []
        self.escalation_note = ""
        self.children: list[ChildLink] = []
        self._in_summary = False
        self._in_rules = False
        self._in_li = False
        self._in_escalation = False
        self._in_esc_text = False
        self._current_link: dict[str, str] | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        amap = {k: (v or "") for k, v in attrs}
        if tag == "main" and "data-rule-id" in amap:
            self.main_attrs = amap
        elif tag == "p" and "rule-summary" in amap.get("class", ""):
            self._in_summary = True
            self._buf = []
        elif tag == "section" and "data-rules" in amap:
            self._in_rules = True
        elif tag == "section" and "data-escalation" in amap:
            self._in_escalation = True
        elif self._in_rules and tag == "li":
            self._in_li = True
            self._buf = []
        elif self._in_escalation and tag in ("p", "li"):
            self._in_esc_text = True
            self._buf = []
        elif tag == "a" and "data-target" in amap:
            self._current_link = amap
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "p" and self._in_summary:
            self.summary = " ".join("".join(self._buf).split())
            self._in_summary = False
        elif tag == "section" and self._in_rules:
            self._in_rules = False
        elif tag == "section" and self._in_escalation:
            self._in_escalation = False
        elif tag == "li" and self._in_li:
            text = " ".join("".join(self._buf).split())
            if text:
                self.rules.append(text)
            self._in_li = False
        elif self._in_esc_text and tag in ("p", "li"):
            text = " ".join("".join(self._buf).split())
            if text:
                self.escalation_note = (
                    f"{self.escalation_note} {text}".strip() if self.escalation_note else text
                )
            self._in_esc_text = False
        elif tag == "a" and self._current_link is not None:
            label = " ".join("".join(self._buf).split())
            self.children.append(
                ChildLink(
                    href=self._current_link.get("href", ""),
                    target=self._current_link.get("data-target", ""),
                    tier=self._current_link.get("data-tier", "mid"),
                    when=self._current_link.get("data-when", ""),
                    label=label,
                )
            )
            self._current_link = None

    def handle_data(self, data: str) -> None:
        if self._in_summary or self._in_li or self._in_esc_text or self._current_link is not None:
            self._buf.append(data)


def extract_ai_block(raw: str) -> str:
    """Return ONLY the semantic block between <!-- AI-RULE-START --> and <!-- AI-RULE-END -->."""
    start_marker = "<!-- AI-RULE-START -->"
    end_marker = "<!-- AI-RULE-END -->"
    if start_marker in raw and end_marker in raw:
        start = raw.index(start_marker) + len(start_marker)
        end = raw.index(end_marker)
        return raw[start:end].strip()
    return raw


def parse_rule_file(path: Path, rules_root: Path) -> RuleNode:
    """Parse one HTML rule file into a structured RuleNode."""
    raw = path.read_text(encoding="utf-8")
    ai_block = extract_ai_block(raw)
    parser = _RuleHTMLParser()
    parser.feed(ai_block)
    a = parser.main_attrs
    if not a.get("data-rule-id"):
        raise ValueError(f"{path} is missing <main data-rule-id='...'> inside AI-RULE block")
    skills = [s.strip() for s in a.get("data-skills", "").split(",") if s.strip()]
    pillars = [p.strip().lower() for p in a.get("data-pillars", "").split(",") if p.strip()]
    keywords = [k.strip().lower() for k in a.get("data-keywords", "").split(",") if k.strip()]
    escalate_when = [
        e.strip() for e in a.get("data-escalate-when", "").split("|") if e.strip() and e.strip() != "none"
    ]
    return RuleNode(
        rule_id=a["data-rule-id"].strip(),
        parent=a.get("data-parent", "").strip(),
        depth=int(a.get("data-depth", "0")),
        title=html.unescape(a.get("data-title", a["data-rule-id"])).strip(),
        tier=a.get("data-tier", "mid").strip(),
        effort=a.get("data-effort", "medium").strip(),
        skills=skills,
        pillars=pillars,
        keywords=keywords,
        escalate_when=escalate_when,
        rel_path=path.relative_to(rules_root).as_posix(),
        escalation_policy=a.get("data-escalation-policy", "").strip(),
        workload=a.get("data-workload", "").strip(),
        summary=parser.summary,
        rules=parser.rules,
        escalation_note=parser.escalation_note,
        children=parser.children,
        ai_bytes=len(ai_block.encode("utf-8")),
        file_bytes=len(raw.encode("utf-8")),
    )


def load_tree(rules_root: Path) -> dict[str, RuleNode]:
    """Load router.html and all branches/**/*.html into a dict keyed by data-rule-id."""
    files = [rules_root / "router.html", *sorted((rules_root / "branches").rglob("*.html"))]
    nodes: dict[str, RuleNode] = {}
    for f in files:
        if not f.is_file():
            continue
        node = parse_rule_file(f, rules_root)
        if node.rule_id in nodes:
            raise ValueError(f"duplicate data-rule-id {node.rule_id!r} in {f}")
        nodes[node.rule_id] = node
    return nodes


def _tokenize(text: str) -> set[str]:
    return {t.lower() for t in TOKEN_PATTERN.findall(text)}


ASCII_SHORT_KW = re.compile(r"^[a-z0-9_-]{1,4}$")
GENERIC_STEM_STOPWORDS = {
    "생성", "요약", "작업", "모델", "분석", "규칙", "설계", "기반", "검증", "방법", "결과", "시스템",
}
ARGUMENT_NUANCE_CUES = ("다각도", "세부 비교", "조건별", "예외 사례", "tradeoff", "nuance")


def _keyword_matches(kw: str, query_lower: str) -> bool:
    """Match keywords safely: short ASCII tags require word boundaries; Korean/phrases allow substring."""
    if ASCII_SHORT_KW.fullmatch(kw):
        return bool(re.search(rf"(?<![a-z0-9_]){re.escape(kw)}(?![a-z0-9_])", query_lower))
    return kw in query_lower


def _score_branch(query_lower: str, query_tokens: set[str], link: ChildLink, node: RuleNode) -> float:
    """Score how well a child node matches a task description."""
    score = 0.0
    for kw in node.keywords:
        if _keyword_matches(kw, query_lower):
            score += 4.0 if " " in kw or len(kw) >= 4 else 2.5
    when_lower = f"{link.when} {link.label} {node.title} {node.summary}".lower()
    when_tokens = _tokenize(when_lower)
    overlap = query_tokens & when_tokens
    score += 2.2 * len(overlap)
    # Stem prefix matching helps inflected Korean tokens (e.g. "논증해줘" <-> "논증", "반론을" <-> "반론").
    for qt in query_tokens - overlap:
        if len(qt) < 2:
            continue
        for wt in when_tokens:
            if len(wt) < 2 or wt in GENERIC_STEM_STOPWORDS or qt in GENERIC_STEM_STOPWORDS:
                continue
            if qt.startswith(wt) or wt.startswith(qt):
                score += 1.6
                break
    return score


def route_top_down(nodes: dict[str, RuleNode], task: str) -> list[RuleNode]:
    """Traverse from root to the deepest matching branch without reading unrelated subtrees."""
    if "root" not in nodes:
        raise ValueError("root node missing")
    q_lower = task.lower()
    q_tokens = _tokenize(task)
    cur = nodes["root"]
    chain = [cur]
    while cur.children:
        best_child: RuleNode | None = None
        best_score = 0.0
        for link in cur.children:
            child = nodes.get(link.target)
            if child is None:
                continue
            sc = _score_branch(q_lower, q_tokens, link, child)
            # Also peek one level deeper so Depth-1 trunks reflect strong Depth-2 matches.
            if child.children:
                deep_best = max(
                    (_score_branch(q_lower, q_tokens, gc, nodes[gc.target]) for gc in child.children if gc.target in nodes),
                    default=0.0,
                )
                sc += 0.75 * deep_best
            if sc > best_score:
                best_score = sc
                best_child = child
        if best_child is None or best_score <= 0.0:
            break
        chain.append(best_child)
        cur = best_child
    return chain


def chain_to_root(nodes: dict[str, RuleNode], branch_id: str) -> list[RuleNode]:
    """Return [root, ..., branch_id] by following data-parent links."""
    if branch_id not in nodes:
        raise KeyError(f"unknown branch id {branch_id!r}; available: {', '.join(sorted(nodes))}")
    chain: list[RuleNode] = []
    seen: set[str] = set()
    cur: RuleNode | None = nodes[branch_id]
    while cur is not None:
        if cur.rule_id in seen:
            raise ValueError(f"cycle detected at {cur.rule_id!r}")
        seen.add(cur.rule_id)
        chain.append(cur)
        cur = nodes.get(cur.parent) if cur.parent else None
    chain.reverse()
    return chain


def resolve_adaptation_profile(leaf: RuleNode) -> tuple[str, str]:
    """Return effective (escalation_policy, workload_profile) for a rule node."""
    rid = leaf.rule_id
    policy = leaf.escalation_policy
    if not policy:
        if rid in ("reasoning.root", "reasoning.simple-argument", "ai-systems.prompt-opt", "meta.model-policy"):
            policy = "overthinking-guard-low"
        elif rid.startswith("research.") or rid == "ai-systems.context-rag":
            policy = "grounding-over-thinking"
        elif leaf.tier == "high" or rid in ("reasoning.structured-argument", "meta.skill-security"):
            policy = "capacity-switch-sensitive"
        else:
            policy = "effort-first-with-verifier"

    workload = leaf.workload
    if not workload:
        if rid == "reasoning.structured-argument":
            workload = "balanced_debate_reasoning"
        elif policy == "grounding-over-thinking":
            workload = "long_context_rag" if leaf.tier != "low" else "fast_extraction"
        elif leaf.tier == "high":
            workload = "frontier_architecture_visual"
        elif leaf.tier == "low":
            workload = "fast_extraction"
        else:
            workload = "verified_coding"
    return policy, workload


def evaluate_difficulty_and_tier(
    leaf: RuleNode,
    *,
    task: str = "",
    files_touched: int = 1,
    attempts: int = 0,
    concurrency: bool = False,
    security: bool = False,
    ambiguity: bool = False,
    has_verifier: bool = True,
) -> dict:
    """Compute difficulty score, apply task-specific Effort-vs-ModelSwitch logic, and recommend tier/effort/skills."""
    policy, workload = resolve_adaptation_profile(leaf)
    base_score = {"low": 20, "mid": 50, "high": 80}.get(leaf.tier, 50)
    score = base_score
    reasons: list[str] = []

    if files_touched >= 4:
        score += 22
        reasons.append(f"coupled_files={files_touched} (>=4)")
    elif files_touched >= 2:
        score += 10
        reasons.append(f"multi_file={files_touched}")
    if attempts >= 2:
        score += 25
        reasons.append(f"failed_attempts={attempts} (>=2)")
    elif attempts == 1:
        score += 12
        reasons.append("retry_attempt=1")
    if concurrency:
        score += 30
        reasons.append("concurrency_or_async_race")
    if security:
        score += 25
        reasons.append("security_or_auth_boundary")
    if ambiguity:
        score += 15
        reasons.append("high_ambiguity")
    t_low = task.lower() if task else ""
    if leaf.rule_id == "reasoning.simple-argument" and any(cue in t_low for cue in ARGUMENT_NUANCE_CUES):
        score += 10
        reasons.append("nuanced_argument_scope")

    score = max(0, min(100, score))
    tier_idx = TIER_ORDER.get(leaf.tier, 1)
    if attempts >= 2 or files_touched >= 4:
        tier_idx = min(2, tier_idx + 1)
    if concurrency or security:
        tier_idx = 2

    # Without an external verifier oracle (tests/compiler), retries hit a Modal Ceiling (arXiv:2606.28661).
    modal_ceiling_hit = (
        not has_verifier
        and policy == "effort-first-with-verifier"
        and (attempts >= 1 or files_touched >= 2 or ambiguity)
    )
    if modal_ceiling_hit:
        tier_idx = min(2, max(tier_idx, TIER_ORDER.get(leaf.tier, 1) + 1))
        reasons.append("no_verifier_modal_ceiling")

    grounding_only = (
        policy == "grounding-over-thinking"
        and ambiguity
        and attempts < 2
        and files_touched < 4
        and not concurrency
        and not security
    )
    if not grounding_only:
        if score >= 75:
            tier_idx = max(tier_idx, 2)
        elif score >= 42:
            tier_idx = max(tier_idx, 1)

    rec_tier = TIER_NAMES[tier_idx]
    escalated = rec_tier != leaf.tier
    if escalated:
        rec_effort = "high" if (rec_tier == "high" or score >= 60) else EFFORT_BY_TIER[rec_tier]
        decision_action = "switch_model_up"
        action_reason = (
            "검증기 부재(Modal Ceiling)로 반복 실패를 막기 위해 상위 모델로 직접 전환"
            if modal_ceiling_hit
            else f"역량·결합도 임계 초과({leaf.tier} → {rec_tier})로 모델 자체 변경 및 {rec_effort} effort 적용"
        )
    elif grounding_only:
        rec_effort = leaf.effort
        decision_action = "ground_before_think"
        reasons.append("grounding_over_thinking_redirect")
        action_reason = "내부 추론(thinking) 증가 시 과잉 확신 위험(arXiv:2508.15050) — 외부 검색·강력한 리랭커 전환(+7.5 NDCG@10) 우선"
    else:
        rec_effort = leaf.effort
        if rec_tier == "low" and score >= 28 and leaf.effort == "low":
            rec_effort = "medium"
            reasons.append("effort_adjusted:low->medium")
        elif rec_tier == "mid" and score >= 60 and leaf.effort != "high":
            rec_effort = "high"
            reasons.append("effort_adjusted:medium->high")
        if rec_effort != leaf.effort:
            decision_action = "raise_effort"
            action_reason = (
                "외부 검증기(테스트/린터) 또는 경미한 조건 상승 구간 — 모델 유지 후 동일 티어 내 Effort 우선 상향"
            )
        else:
            decision_action = "keep_optimal"
            action_reason = (
                "단순 과제 과잉 숙고 역전 방지(arXiv:2504.13367)를 위해 기본 티어·Effort 유지"
                if policy == "overthinking-guard-low"
                else "현재 작업 난이도·정책 기준 최적 모델 티어와 Effort 유지"
            )
    effort_adjusted = (rec_effort != leaf.effort) and not escalated
    skills = list(leaf.skills)
    if rec_tier == "high" and "architecture-rfc" not in skills:
        skills.append("architecture-rfc")
    if not skills and rec_tier == "mid":
        skills.append("targeted-debug")

    pillars = list(leaf.pillars)
    if not pillars:
        pillars = ["prompt"] if rec_tier == "low" else (["harness", "loop"] if rec_tier == "mid" else ["context", "harness", "graph"])
    if task:
        for pname, kws in PILLAR_SIGNALS.items():
            if any(k in t_low for k in kws) and pname not in pillars:
                pillars.append(pname)
    if concurrency and "graph" not in pillars:
        pillars.append("graph")
    if decision_action == "ground_before_think" and "context" not in pillars:
        pillars.append("context")

    return {
        "difficulty_score": score,
        "base_tier": leaf.tier,
        "recommended_tier": rec_tier,
        "recommended_effort": rec_effort,
        "effort_adjusted": effort_adjusted,
        "decision_action": decision_action,
        "action_reason": action_reason,
        "escalation_policy": policy,
        "workload_profile": workload,
        "has_verifier": has_verifier,
        "recommended_skills": skills,
        "recommended_pillars": pillars,
        "escalated": escalated,
        "escalation_reasons": reasons,
    }


def load_model_catalog(rules_root: Path) -> dict:
    cat_path = rules_root / "model-catalog.json"
    if not cat_path.is_file():
        return {}
    return json.loads(cat_path.read_text(encoding="utf-8"))


def load_skill_hierarchy(rules_root: Path) -> dict:
    h_path = rules_root / "skill-hierarchy.json"
    if not h_path.is_file():
        return {}
    return json.loads(h_path.read_text(encoding="utf-8"))


def order_skill_pipeline(skills: list[str], hierarchy: dict) -> tuple[list[str], list[dict]]:
    """Order skills by hierarchy tier and lifecycle phase, resolving requires & conflicts."""
    meta = hierarchy.get("skills", {})
    phases = hierarchy.get("phases", ["gate", "plan", "execute", "verify"])
    phase_idx = {p: i for i, p in enumerate(phases)}

    expanded = list(skills)
    for sk in list(expanded):
        for req in meta.get(sk, {}).get("requires", []):
            if req not in expanded:
                expanded.append(req)

    # Sort by (hierarchy_tier, phase, dependency_depth, name) so prerequisites always precede dependents.
    def dep_depth(sk: str, seen: set[str] | None = None) -> int:
        seen = seen or set()
        if sk in seen:
            return 0
        reqs = meta.get(sk, {}).get("requires", [])
        if not reqs:
            return 0
        return 1 + max(dep_depth(r, seen | {sk}) for r in reqs)

    ordered_raw = sorted(
        dict.fromkeys(expanded),
        key=lambda s: (
            meta.get(s, {}).get("hierarchy_tier", 9),
            phase_idx.get(meta.get(s, {}).get("phase", "execute"), 9),
            dep_depth(s),
            s,
        ),
    )
    accepted: list[str] = []
    blocked: set[str] = set()
    pipeline: list[dict] = []
    for sk in ordered_raw:
        if sk in blocked:
            continue
        info = meta.get(sk, {})
        for c in info.get("conflicts_with", []):
            blocked.add(c)
        accepted.append(sk)
        pipeline.append(
            {
                "name": sk,
                "hierarchy_tier": info.get("hierarchy_tier", 2),
                "phase": info.get("phase", "execute"),
                "role": info.get("role", "domain"),
                "trust": info.get("trust", "unverified"),
            }
        )
    return accepted, pipeline


def approx_tokens(text: str) -> int:
    """Rough cross-tokenizer estimate (~3.6 chars/token for mixed KO/EN HTML/XML)."""
    return max(1, round(len(text.encode("utf-8")) / 3.6))


def format_xml_packet(chain: list[RuleNode], rec: dict, catalog: dict, stats: dict) -> str:
    """Build ultra-compact XML context packet containing ONLY active path rules."""
    leaf = chain[-1]
    tier_info = catalog.get("tiers", {}).get(rec["recommended_tier"], {})
    models = ", ".join(c["model"] for c in tier_info.get("candidates", [])) or rec["recommended_tier"]
    pipe_str = " -> ".join(f"T{p['hierarchy_tier']}:{p['phase']}:{p['name']}" for p in rec.get("skill_pipeline", []))
    lines = [
        f'<active_rule_packet branch="{leaf.rule_id}" depth="{leaf.depth}" '
        f'tier="{rec["recommended_tier"]}" effort="{rec["recommended_effort"]}" '
        f'skills="{",".join(rec["recommended_skills"])}" '
        f'pillars="{",".join(rec["recommended_pillars"])}" '
        f'escalated="{str(rec["escalated"]).lower()}" '
        f'saved_pct="{stats["saved_pct"]}%">',
        f'  <path>{" -> ".join(n.rule_id for n in chain)}</path>',
        f'  <adaptation action="{rec["decision_action"]}" policy="{rec["escalation_policy"]}" workload="{rec["workload_profile"]}">{rec["action_reason"]}</adaptation>',
        f'  <model_candidates role="reference_examples" note="Map tier/effort to actual models available in user runtime">{models}</model_candidates>',
    ]
    if pipe_str:
        lines.append(f"  <skill_pipeline>{pipe_str}</skill_pipeline>")
    if rec["escalation_reasons"]:
        lines.append(f'  <escalation_reasons>{"; ".join(rec["escalation_reasons"])}</escalation_reasons>')
    lines.append("  <rules>")
    for node in chain:
        for rule in node.rules:
            lines.append(f'    <r src="{node.rule_id}">{rule}</r>')
    lines.append("  </rules>")
    if leaf.escalation_note:
        lines.append(f"  <escalate_if>{leaf.escalation_note}</escalate_if>")
    lines.append("</active_rule_packet>")
    return "\n".join(lines)


def resolve(
    rules_root: Path,
    *,
    task: str | None = None,
    branch_id: str | None = None,
    files_touched: int = 1,
    attempts: int = 0,
    concurrency: bool = False,
    security: bool = False,
    ambiguity: bool = False,
    has_verifier: bool = True,
) -> dict:
    """Resolve an active branch chain, recommendation, and context-reduction statistics."""
    nodes = load_tree(rules_root)
    catalog = load_model_catalog(rules_root)
    hierarchy = load_skill_hierarchy(rules_root)
    if branch_id:
        chain = chain_to_root(nodes, branch_id)
    elif task:
        chain = route_top_down(nodes, task)
    else:
        chain = [nodes["root"]]

    leaf = chain[-1]
    rec = evaluate_difficulty_and_tier(
        leaf,
        task=task or "",
        files_touched=files_touched,
        attempts=attempts,
        concurrency=concurrency,
        security=security,
        ambiguity=ambiguity,
        has_verifier=has_verifier,
    )
    ordered_skills, pipeline = order_skill_pipeline(rec["recommended_skills"], hierarchy)
    rec["recommended_skills"] = ordered_skills
    rec["skill_pipeline"] = pipeline
    total_tree_ai_bytes = sum(n.ai_bytes for n in nodes.values())
    total_tree_file_bytes = sum(n.file_bytes for n in nodes.values())
    active_chain_ai_bytes = sum(n.ai_bytes for n in chain)
    stats = {
        "total_nodes": len(nodes),
        "active_nodes": len(chain),
        "total_tree_file_bytes": total_tree_file_bytes,
        "total_tree_ai_bytes": total_tree_ai_bytes,
        "active_chain_ai_bytes": active_chain_ai_bytes,
        "packet_bytes": 0,
        "packet_tokens_est": 0,
        "total_tree_tokens_est": approx_tokens("x" * total_tree_file_bytes),
        "saved_pct": 0.0,
    }
    packet = format_xml_packet(chain, rec, catalog, stats)
    stats["packet_bytes"] = len(packet.encode("utf-8"))
    stats["packet_tokens_est"] = approx_tokens(packet)
    if total_tree_file_bytes > 0:
        stats["saved_pct"] = round((1.0 - stats["packet_bytes"] / total_tree_file_bytes) * 100, 1)
    packet = format_xml_packet(chain, rec, catalog, stats)
    return {
        "chain": [
            {
                "rule_id": n.rule_id,
                "title": n.title,
                "depth": n.depth,
                "rel_path": n.rel_path,
                "ai_bytes": n.ai_bytes,
                "rules": n.rules,
            }
            for n in chain
        ],
        "recommendation": {
            **rec,
            "model_candidates": catalog.get("tiers", {})
            .get(rec["recommended_tier"], {})
            .get("candidates", []),
        },
        "stats": stats,
        "packet_xml": packet,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Resolve minimal-context HTML branching rules.")
    ap.add_argument("--rules-dir", type=Path, default=Path(__file__).resolve().parent.parent / "rules")
    ap.add_argument("--task", type=str, default="", help="Task description to classify top-down.")
    ap.add_argument("--branch", type=str, default="", help="Explicit branch rule_id (e.g. coding.debugging).")
    ap.add_argument("--files", type=int, default=1, help="Estimated coupled files touched.")
    ap.add_argument("--attempts", type=int, default=0, help="Prior failed attempts on same issue.")
    ap.add_argument("--concurrency", action="store_true", help="Concurrency/async race signal.")
    ap.add_argument("--security", action="store_true", help="Security/auth boundary signal.")
    ap.add_argument("--ambiguity", action="store_true", help="High requirement ambiguity signal.")
    ap.add_argument("--no-verifier", action="store_true", help="Disable automated test/compiler verifier oracle (forces model switch on modal ceiling).")
    ap.add_argument("--format", choices=("xml", "json", "md"), default="xml")
    args = ap.parse_args()

    res = resolve(
        args.rules_dir,
        task=args.task or None,
        branch_id=args.branch or None,
        files_touched=args.files,
        attempts=args.attempts,
        concurrency=args.concurrency,
        security=args.security,
        ambiguity=args.ambiguity,
        has_verifier=not args.no_verifier,
    )
    if args.format == "json":
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.format == "md":
        rec = res["recommendation"]
        st = res["stats"]
        print(f"## Active Branch: `{res['chain'][-1]['rule_id']}`")
        print(f"- **Path**: `{' -> '.join(c['rule_id'] for c in res['chain'])}`")
        print(
            f"- **Recommended**: tier=`{rec['recommended_tier']}`, "
            f"effort=`{rec['recommended_effort']}`, "
            f"skills=`{', '.join(rec['recommended_skills']) or 'none'}`, "
            f"pillars=`{', '.join(rec['recommended_pillars'])}`"
        )
        print(f"- **Context**: {st['packet_bytes']} B (~{st['packet_tokens_est']} tok) vs {st['total_tree_file_bytes']} B total ({st['saved_pct']}% saved)")
        print("### Rules")
        for c in res["chain"]:
            for r in c["rules"]:
                print(f"- [{c['rule_id']}] {r}")
    else:
        print(res["packet_xml"])


if __name__ == "__main__":
    main()
