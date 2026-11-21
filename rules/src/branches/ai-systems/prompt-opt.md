---
rule_id: ai-systems.prompt-opt
parent: "ai-systems.root"
depth: 2
title: "Prompt 중심 설계 (Prompt & Chaining)"
html_title: "Prompt Engineering Branch · HTML Branching Rules"
heading: "Prompt 중심 설계 (Prompt & Chaining)"
tier: low
effort: low
skills: [claim-verify, ai-architecture-stack]
pillars: [prompt]
keywords: [prompt, few-shot, structured output, json schema, pydantic, dspy, prompt chaining, 프롬프트, 구조화 출력, 분류, 추출]
escalation_policy: overthinking-guard-low
workload_profile: fast_extraction
escalate_when: [external_retrieval_needed, dynamic_branching]
---

> 고정 입력→출력 변환, 분류, 구조화 데이터 추출, 순차 Prompt Chaining에 하위 모델을 적용해 최소 지연·비용을 달성합니다.

## Rules: 적용 규칙
- 자유 서술 대신 타입 스키마(JSON Schema/Pydantic)와 명확한 경계 태그(XML)로 출력 형태를 고정한다.
- 단계가 고정된 2~4단계 파이프라인은 자율 루프 대신 코드 게이트가 있는 Prompt Chaining으로 구현한다.
- 반복 컴파일·프롬프트 자동 튜닝이 필요하면 DSPy 시그니처·메트릭 기반 최적화를 적용한다(중위 승격).

## Escalation: 전환/조합 신호
최신 외부 문서나 장기 대화가 필요하면 `context-rag`와 조합하고, 검증 실패 재시도가 필요하면 `agent-loop`로 확장한다.
