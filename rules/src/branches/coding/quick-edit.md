---
rule_id: coding.quick-edit
parent: "coding.root"
depth: 2
title: "단순 편집 · 보일러플레이트 (Quick Edit)"
html_title: "Quick Edit · HTML Branching Rules"
heading: "단순 편집 · 보일러플레이트"
tier: low
effort: low
skills: []
pillars: [prompt]
keywords: [typo, rename, format, boilerplate, lint, snippet, 오타, 포맷, 단순수정, 스니펫, 리네임]
escalation_policy: effort-first-with-verifier
workload_profile: fast_extraction
escalate_when: [logic_change, test_failure, "coupled_files>=2"]
---

> 로직 변경이 없는 단일 파일 수정, 오타 교정, 스타일/포맷 정리에 하위 모델을 배치합니다.

## Rules: 실행 규칙
- 수정 대상 라인 주변만 읽고, 최소 diff로 즉시 패치한다.
- 문법/린트 확인만 수행하고 불필요한 아키텍처 재구성을 금지한다.

## Escalation: 에스컬레이션 기준
동작 로직이 바뀌거나 테스트 실패가 발생하면 즉시 `coding.debugging` (중위 모델)으로 승격한다.
