---
rule_id: coding.architecture
parent: "coding.root"
depth: 2
title: "아키텍처 설계 · 대규모 리팩터링 (Architecture & RFC)"
html_title: "Architecture Branch · HTML Branching Rules"
heading: "아키텍처 설계 · 대규모 리팩터링"
tier: high
effort: high
skills: [architecture-rfc]
pillars: [context, harness, graph]
keywords: [architecture, system design, migration, refactor, security, scalability, 아키텍처, 시스템 설계, 마이그레이션, 대규모 리팩터링, 보안]
escalation_policy: capacity-switch-sensitive
workload_profile: frontier_architecture_visual
escalate_when: []
---

> 다중 모듈 결합, 데이터 스키마/API 마이그레이션, 보안·성능 트레이드오프를 다루는 상위 모델 분기입니다.

## Rules: 실행 규칙
- 구현 전 경계 계약(인터페이스·에러 도메인·호환성)과 대안 2개 이상의 트레이드오프를 먼저 정리한다.
- 단계별 검증 가능한 작은 커밋/패치 단위로 분할하고, 스키마·통합 테스트를 함께 작성한다.
- 핵심 아키텍처 트레이드오프는 `tradeoff.md`에 영속화한다.
