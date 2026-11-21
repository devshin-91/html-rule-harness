---
rule_id: reasoning.deep-synthesis
parent: "reasoning.root"
depth: 2
title: "심층 교차 논증 · 전략 종합 (Deep Synthesis)"
html_title: "Deep Synthesis · HTML Branching Rules"
heading: "심층 교차 논증 · 전략 종합"
tier: high
effort: high
skills: [claim-verify, architecture-rfc]
pillars: [prompt, context]
keywords: [deep synthesis, tradeoff, conflicting evidence, strategy, 반론, 교차 검증, 트레이드오프, 심층 논증, 전략]
escalate_when: []
---

> 상충 근거 대조, 반론 시뮬레이션, 다축 트레이드오프가 요구되는 고난도 논증 분기입니다.

## Rules: 실행 규칙
- 찬성/반대 근거와 대안 옵션을 최소 2축 이상(예: 품질 vs 토큰 비용, 유연성 vs 안전성)으로 비교한다.
- 핵심 결정 근거와 폐기 대안은 `tradeoff.md`에 구조화할 수 있다.
- 모든 핵심 주장은 `claim-verify`로 원문 근거와 대조한 뒤 결론을 확정한다.
