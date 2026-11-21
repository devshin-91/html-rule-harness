---
rule_id: research.fact-lookup
parent: "research.root"
depth: 2
title: "단일 문서 · 시그니처 조회 (Fact Lookup)"
html_title: "Fact Lookup · HTML Branching Rules"
heading: "단일 문서 · 시그니처 조회"
tier: low
effort: low
skills: [claim-verify]
keywords: [lookup, signature, flag, version, single doc, 조회, 시그니처, 옵션 확인]
escalation_policy: grounding-over-thinking
workload_profile: fast_extraction
escalate_when: [missing_in_primary_doc, "sources>=2"]
---

> 단일 공식 문서나 로컬 파일에서 정확한 사실·옵션만 빠르게 추출하는 하위 모델 분기입니다.

## Rules: 실행 규칙
- 대상 파일 또는 공식 문서의 해당 섹션만 읽어 정확한 값/시그니처/경로를 인용한다.
- 문서에 없는 내용은 추론으로 채우지 말고 미확인으로 명시한다.
