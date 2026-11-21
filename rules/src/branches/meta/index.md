---
rule_id: meta.root
parent: "root"
depth: 1
title: "커스텀 규칙 · 모델 · 스킬 위계 정책 (Meta & Harness²)"
html_title: "Meta & Model Policy · HTML Branching Rules"
heading: "커스텀 규칙 · 모델 · 스킬 위계 정책"
tier: mid
effort: medium
skills: [harness-propose-probe-compose, skill-security-audit]
pillars: [harness, graph]
keywords: [meta, custom rule, model policy, tier, skill hierarchy, skill security, anti-hallucination, hallucination, fact-check, 커스텀, 규칙 설계, 모델 추천, 스킬 위계, 악성 스킬, 환각 방지, 환각 검증, 근거 인용]
escalate_when: [framework_redesign]
nav_aria: "메타 세부 분기"
---

> 모델 티어 탐색, 커스텀 분기 빌더, 4계층 스킬 위계, 악성 스킬 검역 및 환각 방지 가드레일을 관장합니다.

## Rules: 메타 규칙
- 새 커스텀 분기는 **Propose → Probe → Compose** 주기와 보안 스캔으로 검증한다.
- 전역 평면 스킬 나열을 금지하고 계층·페이즈·분기 규칙으로만 활성화한다.

## Branches: 세부 분기 (Depth 2)
| target | href | tier | label | when |
| --- | --- | --- | --- | --- |
| `meta.model-policy` | `model-router-policy.html` | `low` | 1. 난이도별 모델 · Effort 정책 | 하위/중위/상위 모델 탐색, Effort/승격 기준, 프론티어 과잉지시 금지 |
| `meta.custom-builder` | `custom-branch-builder.html` | `mid` | 2. 커스텀 작업 분기 빌더 | 특정 작업용 커스텀 복합 분기 규칙 설계, MD/HTML 규칙 노드 추가 |
| `meta.skill-hierarchy` | `skill-hierarchy.html` | `mid` | 3. 스킬 위계 · 분기 · 충돌 해결 | 스킬 위계 구조화, 스킬 간 분기·선행·충돌(SKILLCLASH) 해소 |
| `meta.skill-security` | `skill-security.html` | `mid` | 4. 악성 스킬 차단 · 보안 게이트 | 악성 스킬 탐지, SKILL.md 인젝션·크리덴셜 유출 차단, 외부 스킬 검역 |
| `meta.anti-hallucination` | `anti-hallucination.html` | `high` | 5. 환각 방지 · 근거 인용 검증 | 환각 검증, 근거 인용, 거짓 전제 교정, Gemini 4 Carbon/Argon/Hydrogen 5계보·Tier 0–2 팩트체크 |
