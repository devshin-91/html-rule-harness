---
rule_id: meta.skill-hierarchy
parent: "meta.root"
depth: 2
title: "스킬 위계 · 분기 · 충돌 해결 (Skill Hierarchy & Pipeline)"
html_title: "Skill Hierarchy & Branching · HTML Branching Rules"
heading: "스킬 위계 · 분기 · 충돌 해결"
tier: mid
effort: medium
skills: [rule-router, harness-propose-probe-compose]
pillars: [harness, graph]
keywords: [skill hierarchy, skill clash, skill shadowing, flat skills, vibe coding, superpowers, 스킬 위계, 스킬 분기, 스킬 충돌, 스킬 구조화]
escalate_when: [conflicting_skills, "skill_count>=15"]
---

> 평면적(flat) 스킬 나열로 인한 Skill Shadowing·충돌(SKILLCLASH)을 막기 위해 4계층 위계와 실행 페이즈를 강제합니다.

## Rules: 4계층 스킬 위계 (Tier 0 → 3)
- **Tier 0 (Gate / Meta)**: `rule-router`, `skill-security-audit`, `harness-propose-probe-compose` — 가장 먼저 진입·검역·분기 결정.
- **Tier 1 (Plan / Process)**: `ai-architecture-stack`, `architecture-rfc` — 구현 스킬보다 선행해 설계·아키텍처를 확정.
- **Tier 2 (Execute / Domain)**: `targeted-debug`, `frontier-craft` — 확정된 분기 내에서만 국소/고급 실행.
- **Tier 3 (Verify / Audit)**: `claim-verify`, `anti-hallucination-guard` — 최종 산출물·근거·환각·테스트 검증 후 완료 선언.
- **분기·충돌 해소 (O(depth) Lazy Discovery)**: 평면 목록은 ~50~60개 근방에서 혼동 급락(`arXiv:2601.04748`)과 블랙홀 스킬 편향을 일으키므로, HTML 분기 트리로 활성 자식만 노출(`arXiv:2607.11138`)하고 `rules/skill-hierarchy.json`의 선행(`requires`)·충돌(`conflicts_with`)을 자동 정렬한다(`SkillDAG`).
