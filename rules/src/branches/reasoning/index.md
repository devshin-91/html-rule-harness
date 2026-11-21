---
rule_id: reasoning.root
parent: "root"
depth: 1
title: "논증 · 문서 · 기획 분기 (Reasoning & Synthesis)"
html_title: "Reasoning Branch · HTML Branching Rules"
heading: "논증 · 문서 · 기획 분기"
tier: low
effort: low
skills: [claim-verify]
keywords: [argument, logic, summary, essay, reasoning, synthesis, counterargument, 논증, 요약, 문서, 기획, 설득, 비교, 반론, 찬반]
escalate_when: [conflicting_sources, multi_stakeholder_strategy]
nav_aria: "논증 세부 분기"
---

> 논증도 복잡도에 따라 하위(low)·중위(mid)·상위(high)와 내부 Effort를 분리합니다. 과잉 숙고를 막고 반론·가정 감사에는 중위 이상을 씁니다.

## Rules: 분기 및 Effort 선택 규칙
- 단순 3줄 요약·명확한 1차원 논증은 **과잉 추론 역전(arXiv:2504.13367)**을 피하기 위해 `low / low`를 유지하되, 조건부 비교는 `low / effort:medium`으로 조정한다.
- 찬반 균형·숨은 가정·반론 검토·설득 논증은 `mid`(`structured-argument`), 상충 문헌 교차 종합은 `high`(`deep-synthesis`)로 분기한다.

## Branches: 세부 분기 (Depth 2)
| target | href | tier | label | when | subtitle |
| --- | --- | --- | --- | --- | --- |
| `reasoning.simple-argument` | `simple-argument.html` | `low` | 1. 간단한 논증 생성 (Simple Argument) | 간단한 논증 생성, 단일 주장 정당화, 3줄 핵심 장단점 요약 | 하위 모델(low) · effort low/medium · claim-verify |
| `reasoning.structured-argument` | `structured-argument.html` | `mid` | 2. 구조화 논증 · 반론 검토 (Structured Argument) | 찬반 균형 논증, 예상 반론·재반박, 숨은 가정/논리 허점 점검, 설득 메모 | 중위 모델(mid) · effort medium/high · claim-verify |
| `reasoning.deep-synthesis` | `deep-synthesis.html` | `high` | 3. 심층 교차 논증 · 전략 종합 (Deep Synthesis) | 상충 논문/다중 근거 교차 논증, 고위험 장기 전략, 다축 아키텍처 트레이드오프 종합 | 상위 모델(high) · effort high · claim-verify, architecture-rfc |
