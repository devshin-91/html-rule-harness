---
rule_id: meta.custom-builder
parent: "meta.root"
depth: 2
title: "커스텀 작업 분기 빌더 (Custom Branch Builder)"
html_title: "Custom Branch Builder · HTML Branching Rules"
heading: "커스텀 작업 분기 빌더"
tier: mid
effort: medium
skills: [harness-propose-probe-compose]
keywords: [custom branch, new rule, template, extend, split, 커스텀 분기, 규칙 추가, 확장, 템플릿]
escalate_when: [schema_breaking_change]
---

> 특정 도메인이나 복합 워크플로우 전용의 커스텀 HTML 분기 구조를 Harness² 방식으로 설계·검증합니다.

## Rules: 커스텀 분기 제작 4단계 (Harness² Propose–Probe–Compose)
1. **Propose**: `rules/src/branches/<domain>/<node>.md`에 YAML frontmatter(`rule_id`, `parent`, `depth`, `tier`, `effort`, `skills`, `keywords`)와 최소 실행 규칙을 작성한다.
2. **Link**: 부모 Markdown(`rules/src/.../index.md`)의 `## Branches` 표에 조건부 분기 행 1줄을 추가한다.
3. **Probe**: `python scripts/build_rules_html.py`, `python scripts/validate_harness.py`, `python scripts/resolve_rule.py --task "..."`로 컴파일·토큰 절감률·라우팅을 검증한다.
4. **Compose**: 컴파일된 HTML의 AI 블록(`<!-- AI-RULE-START -->` 내부)을 1,500B 권장(상한 2,800B) 이내로 유지하고, Markdown 단일 소스를 편집 후 재컴파일한다.
