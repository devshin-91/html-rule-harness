---
rule_id: meta.model-policy
parent: "meta.root"
depth: 2
title: "난이도별 모델 · Effort 탐색 정책 (Model Router Policy)"
html_title: "Model Router Policy · HTML Branching Rules"
heading: "난이도별 모델 · Effort 탐색 정책"
tier: low
effort: low
skills: [rule-router]
keywords: [model tier, low, mid, high, effort, escalation, model switch, 하위모델, 중위모델, 상위모델, 모델 변경, 모델 탐색, 난이도]
escalation_policy: overthinking-guard-low
workload_profile: fast_extraction
escalate_when: []
---

> 작업별 역량 하한·검증기 유무·그라운딩 여부에 따라 동일 모델 Effort 상향과 모델 자체 전환을 분리 결정합니다.

## Rules: Effort 상향 vs 모델 변경 결정 정책
- **effort-first-with-verifier** (코딩·루프): 테스트·컴파일러 검증기가 있으면 1회 실패/2–3파일 범위는 동일 모델 **Effort 우선 상향**(`Ma 2025`). 검증기 부재(Modal Ceiling, `arXiv:2606.28661`)나 2회+ 실패·4+파일 시 **모델 상향 전환**(Sonnet→Opus medium).
- **capacity-switch-sensitive** (아키텍처·동시성·반론·보안·탁월한 UI): Reasoning Floor(`arXiv:2504.14047`) 또는 아첨 위험이 있으므로 작은 모델 Effort 증가 대신 상위 모델로 즉시 전환한다.
- **grounding-over-thinking** (리서치·RAG): 사실 누락·검색 부실은 thinking 증가로 악화되므로(`arXiv:2508.15050`) 외부 검색·강력한 리랭커(`+7.5 NDCG@10`)로 전환한다.
- **overthinking-guard-low** (단순 요약·구조화 추출): 역-U자 과잉 숙고(`arXiv:2606.02835`) 차단을 위해 `low/low` 기본 유지 후 필요 시만 조정.
- **모델명 참고·일반 기준선 고지**: 카탈로그 모델명은 티어 예시이며 실제 환경에서 호출 가능한 최신 모델·Effort로 매핑한다(일반 규칙이므로 환경·세부 작업에 따라 효과 편차 가능).

## Human Reference: 프로바이더별 모델 티어 · Effort 제어 카탈로그 (v3.0 Human Reference)
| 티어 / 점수 | Effort / `thinking_level` | 후보 모델군 (Active Only) | 모델 변경 · 특화 전환 기준 |
| --- | --- | --- | --- |
| **low (0–41)** | `minimal` / `low` | `gemini-3.5-flash-lite` · `gemini-decision-1` (`v1beta`) / Claude Haiku / GPT-mini | 과잉 숙고 역전 방지 기본 유지; 폐쇄형 분류는 `client.decisions.create` 우선, 반론/복수 파일 시 `mid` 전환 |
| **mid (42–74)** | `medium`~`high` (`xhigh` on Hydrogen) | `gemini-4-hydrogen` (1M, 기본 `high`) · `gemini-4-neon` / Claude Sonnet / GPT balanced | 테스트 존재 1회 실패 → Effort 상향; `minimal`·명시적 캐싱 미지원; 검증기 부재·문헌 상충 → `high` 전환 |
| **high (75–100)** | `medium`(기본)~`high` | `gemini-4-carbon` · `gemini-4-argon` (1M) / Claude Opus / GPT Frontier | Carbon/Argon은 `xhigh`/`minimal`·명시적 캐싱·픽셀 세그멘테이션 미지원; Long Decode는 `background=True` + `max_output_tokens > 65536` |
