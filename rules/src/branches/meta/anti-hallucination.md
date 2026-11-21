---
rule_id: meta.anti-hallucination
parent: "meta.root"
depth: 2
title: "환각 방지 · 근거 인용 · 5계보 검증 (Anti-Hallucination Guard)"
html_title: "Anti-Hallucination Guard · HTML Branching Rules"
heading: "환각 방지 · 근거 인용 · 5계보 검증"
tier: high
effort: high
skills: [anti-hallucination-guard, claim-verify]
pillars: [harness, context]
keywords: [anti-hallucination, hallucination, fact-check, quote-first, line citation, long decode, gemini-4-carbon, gemini-4-argon, gemini-4-hydrogen, 환각, 환각 방지, 환각 검증, 근거 인용, 원문 발췌, 거짓 전제, 팩트체크]
escalation_policy: capacity-switch-sensitive
workload_profile: anti_hallucination_audit
escalate_when: [unverified_claim, fabricated_param, partial_patch]
---

> 4대 환각 차단 원칙, 5대 모델 계보 스펙 경계, Long Decode 회계 및 Tier 0–2 팩트체크를 강제합니다.

## Rules: 환각 방지 · 근거 인용 핵심 가드레일
- **4대 원칙**: (1) 도구 우선 검증·역환각 금지(로컬→공식 MCP/SKILL→실행 순, 신규 세대 오판 금지), (2) 선 원문 발췌+`#Lstart-Lend` 인용, (3) 미확인 명시·거짓 전제 교정(레거시 1.x/2.x 금지), (4) 해시·날짜·IEEE-754(`Decimal(str(x))`+`ROUND_HALF_UP`)·패치 실행 실측.
- **5계보 경계**: Flash/Lite(`3.8-flash`/`3.5-flash-lite`) `temperature/top_p/top_k` 제거; Hydrogen(`gemini-4-hydrogen`, `low/medium/high(기본)/xhigh`, `minimal`·명시적 캐싱 불가) 핫픽스·엣지 검증; Neon/Pro 구세대·`type` 누락 차단; Argon 미문서화 파라미터 금지·`hmac.compare_digest`; Carbon(`gemini-4-carbon`, `low/medium(기본)/high`, `xhigh/minimal`·명시적 캐싱·픽셀 세그멘테이션 불가) 부분 패치 차단.
- **Long Decode**: `carbon/argon/hydrogen`은 `background=True`+`max_output_tokens > 65536` 동시 필수, `interaction.steps` 결합, `total_input_tokens` 압축 트리거 금지.
- **Tier 0–2 팩트체크**: T0(`#L`·1:1 인용)→T1(SQLite+DOI, 0 tok)→T2(PDF Set-Cover `-90%` tok+Cascade). `Stop` 훅 `max_continuations=2`+인간 승인.

## Human Reference: 5대 모델 계보 · Gemini 4 공식 스펙 & Tier 0–2 팩트체크 기준표
| 계보 / 모델 | `thinking_level` 범위 (기본값) | 미지원 API / 금지 항목 | 핵심 환각 차단 포인트 |
| --- | --- | --- | --- |
| **Flash/Lite** (`gemini-3.5-flash-lite`, `gemini-3.8-flash`) | `minimal`, `low`, `medium`(기본), `high` (`xhigh` 미지원) | `temperature`, `top_p`, `top_k`, `thinking_budget`, `role="model"` prefill | 역환각(신규 세대 부정) 금지, 공식 MCP/SKILL 우선 조회, 다단계 대조 시 `>= medium` |
| **Hydrogen** (`gemini-4-hydrogen`) | `low`, `medium`, `high`(기본), `xhigh` | `minimal` 거부, 명시적 캐싱(`cachedContents`/`caches.create`), 샘플링 파라미터 | 로그 중간 핫픽스 오버라이드 추적, 혼합 대소문자·중복 접두사 엣지 실행 검증 |
| **Neon/Pro** (`gemini-4-neon`) | 로스터 중위 리팩터링·STEM (API 병행: `gemini-4-hydrogen`/`argon`) | 레거시 1.x/2.x 모델 혼용, `agent_config` 필수 `"type"` 누락 | 현역 모델 목록 1:1 대조, 수학·알고리즘 명제는 소규모 반례 먼저 실행 |
| **Argon** (`gemini-4-argon`) | `low`, `medium`(기본), `high` (`xhigh`/`minimal` 미지원) | 명시적 캐싱, 픽셀 세그멘테이션 마스크, 미문서화 가상 파라미터 | 과잉 추론(`continuation_token` 등) 금지, Long Decode 2중 조건·`hmac.compare_digest`+랜덤 Nonce |
| **Carbon** (`gemini-4-carbon`) | `low`, `medium`(기본), `high` (`xhigh`/`minimal` 미지원) | 명시적 캐싱, 픽셀 세그멘테이션 마스크, `total_input_tokens` 압축 트리거 | 유령 완료(부분 패치) 차단, `Decimal(str(x))`+`ROUND_HALF_UP` 전후 실측, Long Decode 다중 홉 회계 준수 |

- **검증 근거**: 5계보 A/B 총점 `380 → 500` (`+31.58%`), Tier 1 DOI 캐시 `4,630.8ms → 72.99ms → 0.73ms` (`0 LLM tok`, 14/14 함정 차단), Tier 2 PDF Set-Cover 입력 토큰 `-90%` (`11,656 → 1,160`), `Stop` 훅 게이트 미프롬프트 함정 누락 `100% → 0%`.
