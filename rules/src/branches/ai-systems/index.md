---
rule_id: ai-systems.root
parent: "root"
depth: 1
title: "AI 유즈케이스 · 기법 스택 (Prompt/Context/Harness/Loop/Graph)"
html_title: "AI Use-Cases Trunk · HTML Branching Rules"
heading: "AI 유즈케이스 · 기법 스택 분기"
tier: mid
effort: medium
skills: [ai-architecture-stack]
pillars: [prompt, context, harness, loop, graph]
keywords: [ai, prompt, context, harness, loop, graph, frontier, rag, agent, 유즈케이스, 프롬프트, 컨텍스트, 하네스, 루프, 그래프, 조합, 최상위]
escalate_when: [multi_pillar_coupling, durable_hitl]
nav_aria: "AI 기법 세부 분기"
---

> 작업 특성에 맞는 단일 기법, 복합 조합, 최상위 모델 크래프트 분기를 선택합니다.

## Rules: 아키텍처 선택 원칙
- 단순 작업에 그래프·루프를 과잉 적용하지 않는다.
- 지식은 Context, 안전은 Harness, 수렴은 Loop, 병렬·재개는 Graph로 분담한다.

## Branches: 세부 분기 (Depth 2)
| target | href | tier | label | when |
| --- | --- | --- | --- | --- |
| `ai-systems.prompt-opt` | `prompt-opt.html` | `low` | 1. Prompt 중심 | JSON/Pydantic 스키마, Prompt Chaining, DSPy |
| `ai-systems.context-rag` | `context-rag.html` | `mid` | 2. Context 중심 | RAG, GraphRAG, Mem0, Compaction, Context Rot |
| `ai-systems.harness-guard` | `harness-guard.html` | `mid` | 3. Harness 중심 | 샌드박스, 훅, 가드레일, Evals, 스캐폴딩 |
| `ai-systems.agent-loop` | `agent-loop.html` | `mid` | 4. Loop 중심 | ReAct, Evaluator-Optimizer, 테스트 자가수정 루프 |
| `ai-systems.graph-orch` | `graph-orch.html` | `high` | 5. Graph 중심 | LangGraph/ADK 그래프, 멀티에이전트, HITL |
| `ai-systems.combo-recipes` | `combo-recipes.html` | `high` | 6. 복합 기법 조합 | 기법 조합(Context+Loop, Harness+Loop, Graph+Harness, CRAG) |
| `ai-systems.frontier-craft` | `frontier-craft.html` | `high` | 7. 최상위 모델 크래프트 | 최상위 모델, 비주얼/UI 크래프트, Anti-Slop, 스크린샷 루프 |
