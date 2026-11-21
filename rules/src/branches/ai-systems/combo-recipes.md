---
rule_id: ai-systems.combo-recipes
parent: "ai-systems.root"
depth: 2
title: "복합 AI 기법 조합 레시피 (Multi-Technique Combinations)"
html_title: "Multi-Technique Combination Recipes · HTML Branching Rules"
heading: "복합 AI 기법 조합 레시피"
tier: high
effort: high
skills: [architecture-rfc, harness-propose-probe-compose, ai-architecture-stack]
pillars: [prompt, context, harness, loop, graph]
keywords: [combination, hybrid, corrective rag, self-rag, deep agent, combo, 기법 조합, 복합 조합, 조합, 결합, 복합, 파이프라인, 스택]
escalate_when: []
---

> 단일 기법만으로 해결되지 않는 실전 AI 유즈케이스를 위한 검증된 기법 조합 패턴입니다.

## Rules: 대표 조합 매트릭스 (Use-Case → Pillar Stack)
- **Prompt + Context** (정밀 추출/질의응답): Hybrid RAG/Mem0 검색 + 스키마 강제 추출(낮은 지연, 단발 정밀도).
- **Context + Loop** (Corrective/Self-RAG): 검색 품질 평가 → 쿼리 재작성 + 압축(Compaction), 메모리 오염·연쇄 환각 차단 게이트.
- **Harness + Loop** (자율 코딩·검증): 최소 권한 Capability Fencing + 테스트 게이트 + 생성자/평가자 분리 Propose–Probe–Compose.
- **Graph + Harness + Context** (장기 멀티에이전트): 결정적 상태 그래프(DAG/Checkpoint) + 노드별 컨텍스트 격리 + 복잡도 기반 모델·RAG 라우팅 + HITL.
