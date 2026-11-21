---
rule_id: ai-systems.agent-loop
parent: "ai-systems.root"
depth: 2
title: "Loop 중심 설계 (ReAct / Evaluator-Optimizer / Retry)"
html_title: "Loop Engineering Branch · HTML Branching Rules"
heading: "Loop 중심 설계 (ReAct / Evaluator-Optimizer / Retry)"
tier: mid
effort: medium
skills: [targeted-debug, ai-architecture-stack]
pillars: [loop]
keywords: [loop, react, reflexion, evaluator optimizer, self-refine, retry, backpressure, 루프, 자가수정, 반복, 피드백, 테스트 루프]
escalation_policy: effort-first-with-verifier
workload_profile: verified_coding
escalate_when: ["attempts>=2", unbounded_cycle, multi_worker_needed]
---

> 명확한 검증 기준(테스트·린터·루브릭)을 통과할 때까지 생성→관찰→수정을 반복 수렴시키는 제어 루프입니다.

## Rules: 적용 규칙
- 모든 루프에는 **명시적 종료 조건**(최대 스텝, 비용 예산, 2회 연속 동일 실패 시 에스컬레이션)을 강제한다.
- 가능하면 LLM 자기평가보다 단위 테스트·타입체크·결정적 검증기(Backpressure)를 루프 게이트로 사용한다(외부 검증 없는 자기성찰은 정답 퇴행 위험 — VERSE/DISC).
- 주관적 품질(번역·문서)은 생성자·검증자·개선자 역할을 별도 컨텍스트/모델로 분리한 Evaluator-Optimizer(MALT 패턴)로 구성한다.

## Escalation: 에스컬레이션 기준
분기 수와 상태 전이가 복잡해지거나 사람 승인(HITL)·체크포인트 재개가 필요하면 `graph-orch` (상위 모델)로 전환한다.
