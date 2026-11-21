---
rule_id: root
parent: ""
depth: 0
title: "HTML 분기형 규칙 루트 라우터 (Root Router)"
html_title: "Rule Router (Root) · HTML Branching Rules"
heading: "HTML 분기형 규칙 루트 라우터"
tier: low
effort: low
skills: [rule-router]
pillars: [context, harness]
keywords: [root, start, classify, route, 분류, 시작]
escalate_when: [multi_domain, ambiguous_scope]
nav_aria: "1차 분기 선택"
---

> 작업 의도·난이도에 맞는 단일 분기만 탐색해 최소 컨텍스트로 규칙·모델·Skill·AI 기법 스택을 적용합니다.

## Rules: 공통 불변 규칙
- 일치하는 단일 분기만 따라가며 CSS/JS·비관련 분기는 읽지 않는다.
- 파일 4+, 2회 실패, 동시성·보안 감지 시 티어·Effort를 상향한다.
- 표기 모델명은 참고 예시이며 실행 환경의 실제 모델·Effort에 맞춰 호출한다(일반 기준선으로 작업·환경별 편차 존재).

## Branches: 1차 도메인 분기
| target | href | tier | label | when |
| --- | --- | --- | --- | --- |
| `reasoning.root` | `branches/reasoning/index.html` | `low` | 1. 논증 · 문서 · 기획 (Reasoning) | 논증 생성, 논리 요약, 보고서, 다중 주장 비교·종합 |
| `coding.root` | `branches/coding/index.html` | `mid` | 2. 코드 · 디버깅 · 아키텍처 (Coding) | 코드 작성, 디버깅, 오류 수정, 리팩터링, 아키텍처 설계 |
| `research.root` | `branches/research/index.html` | `mid` | 3. 리서치 · 출처 검증 (Research) | GitHub/웹/논문 탐색, 팩트 검증, reference 문서화 |
| `ai-systems.root` | `branches/ai-systems/index.html` | `mid` | 4. AI 유즈케이스 · 기법 스택 (AI Systems) | AI 유즈케이스: 프롬프트, 컨텍스트/RAG, 하네스, 루프, 그래프 및 기법 조합 |
| `meta.root` | `branches/meta/index.html` | `mid` | 5. 커스텀 규칙 · 모델 · 환각 정책 (Meta) | 커스텀 분기 규칙, 모델 정책, 스킬 보안, 환각 방지·근거 인용 |
