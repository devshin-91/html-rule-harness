---
rule_id: ai-systems.graph-orch
parent: "ai-systems.root"
depth: 2
title: "Graph 중심 오케스트레이션 (Stateful Graph / Multi-Agent)"
html_title: "Graph Orchestration Branch · HTML Branching Rules"
heading: "Graph 중심 오케스트레이션 (Stateful Graph / Multi-Agent)"
tier: high
effort: high
skills: [architecture-rfc, ai-architecture-stack]
pillars: [graph]
keywords: [graph, langgraph, adk workflow, pydantic graph, multi-agent, fan-out, orchestrator workers, durable, hitl, 그래프, 상태 전이, 멀티에이전트, 병렬]
escalate_when: []
---

> 순환 상태 전이, 병렬 Fan-out/Fan-in, Orchestrator-Workers, 체크포인팅 및 사람 승인(HITL)이 필요한 복합 워크플로우입니다.

## Rules: 적용 규칙
- 노드 간 공유 상태(State Schema)를 최소 불변 필드로 타이핑하고, 서브에이전트 출력은 요약 결과만 상위로 반환한다.
- 전이 토폴로지와 권한 경계(Capability Fencing)를 프롬프트가 아닌 결정적 그래프/엔진 계약으로 고정해 환각 라우팅과 무한 루프를 차단한다(GraphBit/AgentSPEX).
- 장기 실행·실패 복구가 필요하면 Durable Execution 체크포인트와 HITL 인터럽트 경계를 명시적으로 배치한다.
- 단순 순차 작업까지 그래프로 감싸지 말고, 조건부 순환·병렬 분기가 있는 구간만 그래프 노드로 모델링한다.
