# Harness² Experience Log (`EXPERIENCE.md`)

## Iteration 01 → 02: AI-RULE Context Hydration Split (Propose–Probe–Compose)

- **adopted**: `rule-ui-hydration-v2`
- **cue**: HTML 규칙 파일이 사람용 UI 마크업과 AI 메타데이터를 동시에 포함하여 `validate_harness.py`의 AI 블록 상한(2,800B)을 초과함.
- **what each edit did**:
  1. **Propose**: 초기 `router.html`, `debugging.html`, `model-router-policy.html`에 `<div class="rule-eyebrow">`, `<div class="rule-badges">` 및 모델 카탈로그 HTML 표를 `<!-- AI-RULE-START/END -->` 내부에 직접 배치.
  2. **Probe**: `python scripts/validate_harness.py` 실행 결과 3개 파일이 2,800B 초과(`router.html` 3,245B, `debugging.html` 2,837B, `model-router-policy.html` 3,341B)로 차단됨을 관측.
  3. **Compose**: 중복 시각 배지 마크업을 AI 블록에서 제거하고 `rules/assets/rule-ui.js`가 `data-depth`/`data-tier`/`data-effort`/`data-skills`로부터 자동 렌더링하도록 분리. 모델 카탈로그 표는 `<!-- AI-RULE-END -->` 바깥(Human Reference)으로 이동.
- **lesson**: 듀얼 오디언스(AI + Human) HTML에서는 **기계가 읽는 시맨틱 속성(`data-*`)이 단일 원천(Single Source of Truth)**이 되고, 시각 장식 DOM은 외부 JS/CSS가 하이드레이션할 때 AI 컨텍스트 손실과 UI 품질 충돌을 동시에 해결할 수 있다.
- **evidence**: `validate_harness.py` 재검증 및 `resolve_rule.py` 프로브에서 활성 패킷 절감률 94.9%~95.6% 달성.
- **confidence**: high

## Iteration 02 → 03: Depth Bound & Cascade Routing (Liner Scholar Grounded)

- **adopted**: `depth-cap-3-and-cascade`
- **cue**: 분기를 무한정 깊게 중첩하면 컨텍스트는 줄어도 다단계 LLM 라우팅 정확도가 하락할 수 있음 (`arXiv:2607.17598`).
- **what each edit did**:
  1. `validate_harness.py`에 `RECOMMENDED_MAX_DEPTH = 3` 경고를 도입해 과도한 깊이 분기를 조기 감지.
  2. `resolve_rule.py`와 `meta/model-router-policy.html`을 `arXiv:2410.10347`의 Cascade Routing 모델로 정렬(초기 `low/mid` 라우팅 + 실패/결합도 신호 시 `high` 승격).
- **lesson**: HTML 분기는 최대 Depth 3(Root → Domain → Sub-branch → Leaf) 이내로 넓이와 깊이를 균형 있게 설계하고, 결정적 스크립트(`resolve_rule.py`)로 활성 경로를 단일 패킷으로 평탄화해 주입한다.
- **evidence**: Liner Scholar 조사 논문 (`arXiv:2607.17598`, `arXiv:2410.10347`) + `tests/test_rules_harness.py` 5건 통과.
- **confidence**: high

## Iteration 03 → 04: AI Use-Cases Trunk & Branch-Link Prose Deduplication

- **adopted**: `ai-usecases-5-pillars-v4`
- **cue**: `router.html`에 5번째 도메인(`ai-systems.root`)을 추가하고 `ai-systems/index.html`에 6개 기법 분기를 넣자 두 라우터 파일의 AI 블록이 `2,800B` 상한을 초과함(`2,984B`, `3,598B`).
- **what each edit did**:
  1. **Propose**: 5대 기법(Prompt/Context/Harness/Loop/Graph) 및 복합 조합(`combo-recipes.html`) 분기와 `data-pillars` 속성을 신설.
  2. **Probe**: `validate_harness.py`가 `router.html`과 `ai-systems/index.html`의 2,800B 초과를 감지. 원인: `<a class="branch-link">` 내부에 `data-when`과 `<span>` 설명이 중복됨.
  3. **Compose**: 라우터 링크 안의 중복 `<span>`을 제거하고 `rule-ui.js`가 `data-tier`로부터 기본 티어 배지를 자동 렌더링하도록 전환.
- **lesson**: 라우터 링크 목록이 넓어질수록(5~6개 분기), 링크 내부의 인간용 보조 설명은 `data-*` 기반 JS 렌더링으로 넘겨야 Depth 1 라우터의 상한(`<= 2,800B`)을 깨지 않고 확장성을 유지할 수 있다.
- **evidence**: `validate_harness.py` Error 0 (`router.html` 2,445B, `ai-systems/index.html` 2,757B), `tests/test_rules_harness.py` 6/6 통과.
- **confidence**: high

## Iteration 04 → 05: Empirical Argument Effort Calibration & Zero-Slop UI Overhaul

- **adopted**: `two-stage-effort-and-editorial-ui-v5`
- **cue**: (1) 사용자 스크린샷에서 `"간단한 논증..."` 입력 상태와 수동 클릭된 `frontier-craft` 결과가 배너 없이 겹쳐 보였고, CSS Grid `min-width: auto`로 인해 XML 패킷·스킬 배지·프리셋 행이 가로 잘림. (2) 논증이 무조건 `low`라는 단순 가정이 반론/아첨/허점 감사에서 깨짐(`arXiv:2509.16533`, `arXiv:2508.15050`), (3) `"exceptional"` 한국어 번역이 `"예외적"`으로 오역됨.
- **what each edit did**:
  1. `structured-argument.html`(`mid/medium`) 추가 및 `resolve_rule.py`/`rule-ui.js`에 티어 승격 전 Effort 우선 보정(`28–41: low→medium`, `60–74: mid→high`), 단어경계·한국어 어간 매칭, 명시적 `수동 분기 탐색 중` 배너 추가.
  2. Warm Paper(`#F6F5F0`) + Forest Teal(`#0F766E`) + Lucide(ISC)·Pretendard/JetBrains Mono(SIL OFL 1.1) 기반 무잘림 UI 개편 및 푸터·`reference/` 크레딧 기록.
- **lesson**: 탐색형 트리에서 노드 직접 선택은 반드시 자동 라우팅과 시각적으로 격리해야 상태 오인을 막고, 논증 역시 단순 요약(`low`·과잉 추론 금지) vs 반론 검토(`mid`) vs 문헌 충돌(`high`)로 실증 분리해야 한다.
- **evidence**: `validate_harness.py` (27 노드), `scan_skills_security.py`, `tests/test_rules_harness.py` (11/11), Playwright 다중 뷰포트 시각 검증.
- **confidence**: high

## Iteration 05 → 06: Per-Task Effort Scaling vs. Model Switching (Modal Ceiling & Grounding)

- **adopted**: `per-task-effort-vs-model-switch-v6`
- **cue**: 단순히 난이도 점수만으로 Effort 또는 모델 티어를 일률적으로 올리면, (a) 테스트 검증기가 없는 코딩 작업은 작은 모델에서 모달 천장(`arXiv:2606.28661`)에 갇혀 오답을 반복하고, (b) RAG/사실 조회 작업은 thinking 증가로 오히려 과잉 확신(`arXiv:2508.15050`)과 비효율이 커짐.
- **what each edit did**:
  1. `model-catalog.json`과 `resolve_rule.py`/`rule-ui.js`에 4대 작업별 정책(`effort-first-with-verifier`, `capacity-switch-sensitive`, `grounding-over-thinking`, `overthinking-guard-low`)과 `has_verifier`(`--no-verifier`) 신호를 도입.
  2. 외부 검증기가 있는 1회 실패는 동일 티어 `Effort` 우선 상향(`raise_effort`), 검증기 부재·2회+ 실패·역량 하한 미만은 모델 티어 전환(`switch_model_up`), RAG/사실 모호성은 검색·리랭커 전환(`ground_before_think`)으로 분기.
- **lesson**: "언제 Effort를 올리고 언제 모델 자체를 바꿀지"는 고정 점수가 아니라 **(1) 외부 검증기 유무, (2) 사전학습 역량 하한, (3) 검색 vs 추론 성격**에 의해 갈린다.
- **evidence**: Liner Scholar 6차 논문군(`arXiv:2408.03314`, `2503.20522`, `2606.28661`, `2603.14635`, `2608.08528`) + `validate_harness.py` + `tests/test_rules_harness.py` (12/12).
- **confidence**: high


## Iteration 06 → 07: Live A/B Effectiveness Benchmark & Resumable Checkpoint Cache

- **adopted**: `ab-benchmark-argon-checkpoint-v7`
- **cue**: HTML 분기형 규칙 시스템과 작업별 모델·Effort 동적 매핑(그룹 B)이 실제로 순수 Google Harness² + 단일 고정 모델(`Gemini 4 Argon (Medium)`, 그룹 A) 대비 토큰·시간·품질을 개선하는지 실증 검증이 필요함.
- **what each edit did**:
  1. 복합 엔지니어링 과제(`T1` 논증 요약, `T2` 스키마 빠른 수정, `T3` 런타임 디버깅 3건, `T4` 비동기 동시성 레이스 컨디션 디버깅)와 중단 복구용 체크포인트 캐시(`benchmark/cache/ab_checkpoint.json`), 자동 검증기(`benchmark/ab_harness.py`)를 구축.
  2. 그룹 A(4개 워커 모두 `gemini-4-argon-medium` + 전체 규칙 로드)와 그룹 B(`resolve_rule.py` 단일 `<active_rule_packet>` + `gemini-4-argon-{low,medium,high}` 동적 매핑)를 실측 실행하고 트랜스크립트 텔레메트리를 집계.
- **lesson**: 단일 `<active_rule_packet>` 주입은 규칙 컨텍스트를 96.7% 절감할 뿐 아니라, 전체 규칙 덤프에서 발생하던 **규칙 희석(Context Rot — T3 회귀 테스트 누락, T4 기존 주석 임의 삭제, T1 과잉 장문 생성)**을 막아 입력 토큰 **-33.9%**, 총 토큰 **-31.3%**, 품질 점수 **92점 → 100점**을 동시에 달성한다.
- **evidence**: `benchmark/AB_BENCHMARK_REPORT.md`, `benchmark/cache/ab_checkpoint.json` (8개 워커 실측 트랜스크립트 로그).
- **confidence**: high
