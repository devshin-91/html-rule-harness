---
rule_id: ai-systems.context-rag
parent: "ai-systems.root"
depth: 2
title: "Context 중심 설계 (RAG / Memory / Compaction)"
html_title: "Context Engineering Branch · HTML Branching Rules"
heading: "Context 중심 설계 (RAG / Memory / Compaction)"
tier: mid
effort: medium
skills: [claim-verify, ai-architecture-stack]
pillars: [context]
keywords: [context, rag, graphrag, mem0, memory, compaction, progressive disclosure, 컨텍스트, 검색, 장기 기억, 요약 압축, 토큰 오염]
escalation_policy: grounding-over-thinking
workload_profile: long_context_rag
escalate_when: [query_reformulation_loop, global_corpus_graph]
---

> 대용량 문서, 장기 세션 기억, 툴 출력 비대화(Context Rot) 문제를 검색·압축·계층 메모리로 해결합니다.

## Rules: 적용 규칙
- 컨텍스트 창을 유한 예산으로 취급해 정적 문서 덤프 대신 Progressive Disclosure·Top-K 하이브리드 검색(BM25+벡터+엔티티)을 사용한다.
- 장기 실행 시 오래된 툴 결과 제거(Tool-Result Clearing), 요약 압축(Compaction), 세션·사용자 메모리 계층(Mem0 패턴)을 분리한다.
- 단순 사실 조회는 Dense/Hybrid Vector RAG로 처리하고, 검색 누락 시 thinking 토큰을 늘리기보다 리랭커 모델 강화(`+7.5 NDCG@10`)와 다중 홉만 GraphRAG로 라우팅한다(`arXiv:2603.14635`).

## Escalation: 조합 신호
검색 품질이 1회 조회로 불충분하면 `Corrective RAG (Context + Loop)` 조합으로 승격한다.
