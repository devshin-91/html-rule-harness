---
rule_id: reasoning.structured-argument
parent: "reasoning.root"
depth: 2
title: "구조화 논증 · 반론 검토 (Structured Argument)"
html_title: "Structured Argument · HTML Branching Rules"
heading: "구조화 논증 · 반론 검토"
tier: mid
effort: medium
skills: [claim-verify]
pillars: [prompt, context]
keywords: [structured argument, counterargument, rebuttal, fallacy, policy memo, persuasion, 균형 논증, 찬반, 반론, 재반박, 숨은 가정, 논리 허점, 타당성, 비교 논증, 설득]
escalation_policy: capacity-switch-sensitive
workload_profile: balanced_debate_reasoning
escalate_when: [conflicting_sources, sycophancy_risk, ambiguity]
---

> 찬반 비교·반론 재반박·숨은 가정/논리 허점 감사가 필요한 논증에 중위 모델과 가변 Effort를 배치합니다.

## Rules: 실행 규칙 (Balanced Reasoning & Effort Calibration)
- **최강 반론 우선(Steelman)**: 주장 → 핵심 근거 → 숨은 가정 → 예상 반론 및 재반박 → 적용 조건 순으로 대칭 붕괴를 막는다.
- **아첨·동조 편향 차단**: 후속 반론 제시 시 근거 없이 입장을 뒤집지 않는다(`arXiv:2509.16533`). 모호성·다회 반박 시 Effort를 `high`로 조정한다.
- **외부 검색 그라운딩**: 추론 토큰 증가만으로는 사실 확신 보정이 악화되므로(`arXiv:2508.15050`) `claim-verify`로 사실 근거를 확인한다.

## Escalation: 에스컬레이션 기준
상충하는 1차 논문/문헌 간 종합 판정이나 고위험 장기 전략이 필요하면 `reasoning.deep-synthesis`(`high`)로 승격하고, 단순 3줄 요약·단일 전제 정리는 `reasoning.simple-argument`(`low`)로 내린다.
