---
rule_id: reasoning.simple-argument
parent: "reasoning.root"
depth: 2
title: "간단한 논증 생성 (Simple Argument)"
html_title: "Simple Argument · HTML Branching Rules"
heading: "간단한 논증 생성"
tier: low
effort: low
skills: [claim-verify]
pillars: [prompt]
keywords: [simple argument, short draft, pros cons, summary, 간단한 논증, 논증 생성, 단순 요약, 초안, 3줄 요약]
escalation_policy: overthinking-guard-low
workload_profile: fast_extraction
escalate_when: [counterargument, conflicting_sources, "external_citations>=4"]
---

> 전제가 명확한 단건 논증·3줄 요약에 하위 모델(low)을 배치하며, 과잉 추론으로 정답이 뒤집히는 현상(arXiv:2606.02835)을 방지합니다.

## Rules: 실행 규칙 (Minimal Context)
- 출력 구조는 **전제 → 핵심 근거 → 결론 → 적용 한계(1줄)** 순으로 간결하게 유지한다.
- 단순 논증에 과잉 CoT를 강제하면 오히려 오류가 증가하므로(`arXiv:2502.07266`) `low`를 기본값으로 두고, 다각도 조건 비교 시에만 Effort를 `medium`으로 상향한다.
- 제공되지 않은 수치나 외부 인용을 추측으로 생성하지 않는다.

## Escalation: 에스컬레이션 기준
반론 재반박·숨은 가정 감사가 필요하면 `reasoning.structured-argument`(중위 모델)로, 상충 문헌 교차 종합은 `reasoning.deep-synthesis`(상위 모델)로 전환한다.
