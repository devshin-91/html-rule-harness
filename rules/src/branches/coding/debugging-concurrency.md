---
rule_id: coding.debugging.concurrency
parent: "coding.debugging"
depth: 3
title: "동시성 · 비동기 · 분산 버그 (Concurrency & Race)"
html_title: "Concurrency Debugging · HTML Branching Rules"
heading: "동시성 · 비동기 · 분산 버그"
tier: high
effort: high
skills: [targeted-debug, architecture-rfc]
pillars: [harness, loop, graph]
keywords: [race condition, deadlock, async, thread, lock, distributed, flaky, 동시성, 레이스, 비동기, 데드락, 분산]
escalation_policy: capacity-switch-sensitive
workload_profile: frontier_architecture_visual
escalate_when: []
---

> 비결정적 타이밍·락 순서·상태 불일치가 얽힌 디버깅으로 상위 모델과 high effort로 에스컬레이션합니다.

## Rules: 말단 실행 체크리스트
- 상태 전이(State Transition), 락 획득 순서, 비동기 취소/타임아웃 경계를 먼저 표로 도식화한다.
- 임시 `sleep`으로 타이밍을 회피하지 말고 결정적 동기화/원자적 연산으로 원인을 제거한다.
- 반복 스트레스 테스트(N회 루프)로 간헐적 실패 재현·소멸을 확인한다.
