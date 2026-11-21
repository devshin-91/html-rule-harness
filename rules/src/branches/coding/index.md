---
rule_id: coding.root
parent: "root"
depth: 1
title: "코드 · 디버깅 · 아키텍처 분기 (Coding & Engineering)"
html_title: "Coding Branch · HTML Branching Rules"
heading: "코드 · 디버깅 · 아키텍처 분기"
tier: mid
effort: medium
skills: [targeted-debug]
keywords: [code, coding, edit, debug, fix, refactor, architecture, 코드, 개발, 구현, 디버깅, 수정, 설계]
escalate_when: ["coupled_files>=4", concurrency_or_security]
nav_aria: "코딩 세부 분기"
---

> 작업의 결합도·오류 재현 여부·아키텍처 리스크에 따라 하위/중위/상위 모델 분기로 세분화합니다.

## Rules: 코딩 공통 규칙
- 전체 파일 읽기 전 `rg` 등 검색으로 대상 심볼·호출부만 먼저 위치 특정한다.
- 기존 주석·독스트링을 임의로 삭제하지 않으며, 테스트 통과는 최종 수정 이후 실행 결과로만 확인한다.

## Branches: 세부 분기 (Depth 2)
| target | href | tier | label | when | subtitle |
| --- | --- | --- | --- | --- | --- |
| `coding.quick-edit` | `quick-edit.html` | `low` | 단순 편집 · 보일러플레이트 (Quick Edit) | 오타 수정, 포맷팅, 단일 함수 리네임, 단순 보일러플레이트 | 하위 모델(low) · effort low · 추가 스킬 불필요 |
| `coding.debugging` | `debugging.html` | `mid` | 디버깅 · 코드 수정 (Debugging & Patch) | 디버깅, 버그 수정, 오류/예외 원인 분석, 코드 패치 및 회귀 검증 | 중위 모델(mid) · effort medium · targeted-debug |
| `coding.architecture` | `architecture.html` | `high` | 아키텍처 설계 · 대규모 리팩터링 (Architecture) | 다중 모듈 설계, 시스템 리팩터링, API/스키마 마이그레이션, 보안·성능 최적화 | 상위 모델(high) · effort high · architecture-rfc |
