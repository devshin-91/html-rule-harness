---
rule_id: coding.debugging
parent: "coding.root"
depth: 2
title: "디버깅 · 코드 수정 (Debugging & Patch)"
html_title: "Debugging Branch · HTML Branching Rules"
heading: "디버깅 · 코드 수정"
tier: mid
effort: medium
skills: [targeted-debug]
pillars: [harness, loop]
keywords: [debug, debugging, bug, fix, patch, error, exception, traceback, test fail, 디버깅, 코드 수정, 버그, 오류, 에러, 패치]
escalate_when: ["attempts>=2", "coupled_files>=4", concurrency_or_security]
nav_aria: "디버깅 하위 분기"
---

> 재현 가능한 버그와 국소 코드 수정에 중위 모델 + medium effort + targeted-debug를 권장합니다.

## Rules: 적용 규칙
- 수정 전 최소 재현 커맨드/테스트로 실제 오류 원인을 먼저 확인한다.
- 원인 지점만 최소 변경하고 무관한 주변 리팩터링을 금지한다.
- 수정 후 실패 테스트 + 회귀 테스트를 재실행한다.

## Escalation: 상위 모델 에스컬레이션
동일 수정 2회 실패, 결합 파일 4+, 또는 동시성·보안 이슈 시 `high` 티어로 상향한다.

## Branches: 세부 분기 (Depth 3)
| target | href | tier | label | when | subtitle |
| --- | --- | --- | --- | --- | --- |
| `coding.debugging.runtime` | `debugging-runtime.html` | `mid` | 런타임 · 로직 버그 | 단일 모듈 예외, 스택 트레이스, 타입/로직 버그, 단위 테스트 실패 | 중위 모델(mid) · medium · targeted-debug |
| `coding.debugging.concurrency` | `debugging-concurrency.html` | `high` | 동시성 · 비동기 · 분산 버그 | 레이스 컨디션, 데드락, 비동기 타이밍, 분산 상태 불일치 | 상위 모델(high) · high · targeted-debug, architecture-rfc |
