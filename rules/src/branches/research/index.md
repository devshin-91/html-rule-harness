---
rule_id: research.root
parent: "root"
depth: 1
title: "리서치 · 출처 검증 분기 (Research & Audit)"
html_title: "Research Branch · HTML Branching Rules"
heading: "리서치 · 출처 검증 분기"
tier: mid
effort: medium
skills: [claim-verify]
keywords: [research, paper, github, docs, reference, verify, 리서치, 논문, 웹문서, 레퍼런스, 탐색, 검증]
escalate_when: [cross_paper_synthesis, primary_source_conflict]
nav_aria: "리서치 세부 분기"
---

> 단일 사실 조회부터 GitHub·웹 문서·학술 논문 교차 검증 및 `reference/` 체계화까지 난이도별로 분기합니다.

## Rules: 리서치 공통 규칙
- 실제로 열람·검증한 저장소, 문서, 논문만 `reference/`에 체계화하고 URL·식별자를 명시한다.
- Liner Scholar 호출 전 반드시 잔여 크레딧(> 100)을 먼저 확인하며, 100 이하이면 즉시 중단한다.

## Branches: 세부 분기 (Depth 2)
| target | href | tier | label | when | subtitle |
| --- | --- | --- | --- | --- | --- |
| `research.fact-lookup` | `fact-lookup.html` | `low` | 단일 문서 · 시그니처 조회 (Fact Lookup) | 단일 API 시그니처, CLI 플래그, 1개 문서 내 팩트 확인 | 하위 모델(low) · effort low · claim-verify |
| `research.multi-source-audit` | `multi-source-audit.html` | `mid` | 다중 출처 감사 · 레퍼런스 체계화 (Multi-Source Audit) | GitHub 저장소 비교, 학술 논문 탐색, 다중 문서 교차 검증 및 reference 문서화 | 중위 모델(mid) · effort medium · claim-verify |
