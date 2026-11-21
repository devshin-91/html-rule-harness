---
rule_id: ai-systems.harness-guard
parent: "ai-systems.root"
depth: 2
title: "Harness 중심 설계 (Sandbox / Hooks / Evals)"
html_title: "Harness Engineering Branch · HTML Branching Rules"
heading: "Harness 중심 설계 (Sandbox / Hooks / Evals)"
tier: mid
effort: medium
skills: [harness-propose-probe-compose, ai-architecture-stack]
pillars: [harness]
keywords: [harness, guardrails, sandbox, hooks, evals, middleware, scaffolding, 하네스, 가드레일, 샌드박스, 훅, 평가, 검증]
escalate_when: [production_policy, multi_agent_isolation]
---

> 모델 가중치 변경 없이 툴 인터페이스, Pre/Post 훅, 샌드박스, 결정적 스크립트, Evals로 에이전트 신뢰성을 강제합니다.

## Rules: 적용 규칙 (Google Harness² 원칙)
- 산문 규칙으로만 강제하지 말고 모델이 우회할 수 없는 결정적 훅(`PreToolUse`/`PostToolUse`)과 스키마 검증기를 둔다.
- 생성자와 평가자(Review Subagent / Grader)의 컨텍스트를 분리해 확증 편향을 막는다.
- 반복 기계 작업은 `scripts/*.py`로 내리고, 개선 이력은 `Propose–Probe–Compose`와 경험 라이브러리에 축적한다.
