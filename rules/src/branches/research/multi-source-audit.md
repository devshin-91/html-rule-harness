---
rule_id: research.multi-source-audit
parent: "research.root"
depth: 2
title: "다중 출처 감사 · 레퍼런스 체계화 (Multi-Source Audit)"
html_title: "Multi-Source Audit · HTML Branching Rules"
heading: "다중 출처 감사 · 레퍼런스 체계화"
tier: mid
effort: medium
skills: [claim-verify]
pillars: [context, loop]
keywords: [github, arxiv, scholar, audit, compare, reference, 논문, 저장소, 교차 검증, 문서화]
escalation_policy: grounding-over-thinking
workload_profile: long_context_rag
escalate_when: [contradictory_papers, synthesis_design]
---

> GitHub 저장소, 웹 문서, Liner Scholar 논문을 대조하고 `reference/`에 구조화하는 중위 분기입니다.

## Rules: 실행 규칙
- 실제 구현에 기여한 1차 자료(코드·README·논문 원문)만 `reference/`에 카테고리별 `.md`로 기록한다.
- Liner Scholar 실행 전 잔여 크레딧(> 100)을 확인하고, 사용 후 잔액 변화도 기록한다.
- 상충 주장이나 아키텍처 통합 설계가 필요하면 `reasoning.deep-synthesis` (상위 모델)로 상향한다.
