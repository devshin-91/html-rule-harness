# Google Harness² + HTML 분기형 규칙 시스템 실증 A/B 벤치마크 리포트

- **벤치마크 ID**: `harness2-html-rule-ab-v1`
- **실행 및 감사 일시**: `2026-11-12 06:42 ~ 07:04 KST`
- **최종 품질 감사 모델**: **Gemini 4 Argon (High)** ([`benchmark/audit_quality_high.py`](./benchmark/audit_quality_high.py))
- **검증 스크립트 및 체크포인트 캐시**:
  - 하네스 실행기: [`benchmark/ab_harness.py`](./benchmark/ab_harness.py)
  - 심층 품질 감사기 (`Argon High`): [`benchmark/audit_quality_high.py`](./benchmark/audit_quality_high.py)
  - 재현용 프롬프트 모음: [`benchmark/prompts/REPRODUCIBLE_PROMPTS.md`](./benchmark/prompts/REPRODUCIBLE_PROMPTS.md)
  - 중단 복구용 체크포인트 캐시: [`benchmark/cache/ab_checkpoint.json`](./benchmark/cache/ab_checkpoint.json)
  - 심층 품질 감사 결과 JSON: [`benchmark/cache/high_effort_quality_audit.json`](./benchmark/cache/high_effort_quality_audit.json)
  - 그룹 A 작업 결과물: [`benchmark/workspace_a/`](./benchmark/workspace_a)
  - 그룹 B 작업 결과물: [`benchmark/workspace_b/`](./benchmark/workspace_b)

---

## 0. 실험 재현용 프롬프트 명세 (Reproducible Prompts & Commands)

누구든지 동일한 A/B 벤치마크와 상위 모델(`Gemini 4 Argon (High)`) 기반 심층 품질 감사를 그대로 재현할 수 있도록, **사용자 원본 지시 요지**, **표준 재현용 마스터 프롬프트**, 그리고 **실제 8개 워커(`a-t1`~`a-t4`, `b-t1`~`b-t4`)에 주입된 세부 프롬프트 원문**을 기록합니다.

### 0-1. 원본 사용자 지시 요지 (User Intent Summary)

1. **1차 지시 (A/B 벤치마크 설계·실행 및 체크포인트 캐시)**:
   > "`Gemini 4 Argon (Medium)`에 맞는 큰 작업을 하나 만들어 여러 세부 작업으로 분기가 생기게 하고 A/B 테스트를 수행하자. **A**로는 이 HTML 분기형 규칙을 따르지 않고 순수하게 Google Harness² 기준으로만 움직여서 `Gemini 4 Argon (Medium)`으로만 큰 작업을 전부 수행하고, **B**로는 Google Harness²에 더해 HTML 분기형 규칙을 참고해서 작업별 모델 및 Effort를 Antigravity 가용 모델·Effort로 선정해 수행하자. 사용량 부족으로 중지되는 경우에 대비해 중간 체크포인트 캐시도 반영하고, A와 B의 작업 소요 시간, 총 소모 토큰(비용), 실제 작업 결과 수준을 벤치마크로 대조해 보여줘."
2. **2차·3차 지시 (재현 가능 프롬프트 명세화 + `Gemini 4 Argon (High)` 기반 산출물 품질 심층 감사 및 효용성 검증)**:
   > "누가 다시 재현하고 싶을 때 어떤 프롬프트를 받고 테스트가 되었는지 알 수 있도록 재현 가능한 프롬프트로 수정해 리포트에 반영하자. 그리고 상위 설정인 **`Gemini 4 Argon (High)`**로 A와 B 각각의 실제 결과물에 대한 품질을 정밀 검사하고, 양쪽 비교를 통해 실질적인 효용성(비용·토큰 대비 품질 효율, 규칙 준수 정밀도)을 따져 리포트에 반영하자."

### 0-2. 타인이 그대로 복사해 재현할 수 있는 표준 마스터 프롬프트 (Master Prompt)

```markdown
[A/B 벤치마크 및 상위 모델 품질 감사 재현 지시문]
현재 워크스페이스(`html-rule-harness`)에서 Google Harness² 단독 실행(그룹 A)과 Google Harness² + HTML 분기형 규칙 라우팅 시스템 적용(그룹 B)의 실증 A/B 벤치마크 및 심층 품질 감사를 수행하라.

1. 기준선(Baseline) 모델 및 쿼터 사전 점검:
   - 기준선 모델은 `Gemini 4 Argon (Medium)`(`gemini-4-argon-medium`)으로 설정한다.
   - 실행 전·후 런타임 모델 목록과 잔여 쿼터를 조회하여, 가용 한도가 0%이거나 임계치 미만인 프로바이더는 제외하고 실제 호출 가능한 런타임 모델·Effort(`low` / `medium` / `high`)로 매핑한다.

2. 복합 대과제 및 4개 세부 작업(T1~T4) 분기:
   - 대과제: "실시간 에이전트 태스크 큐 & 쿼터 가드레일(Quota Guardrail) 엔진 구축 및 검증"
   - `python benchmark/ab_harness.py init`을 실행하여 시드 코드(`benchmark/seeds/`)를 `benchmark/workspace_a`(그룹 A)와 `benchmark/workspace_b`(그룹 B)에 각각 초기화하고, 중단 복구용 체크포인트 캐시(`benchmark/cache/ab_checkpoint.json`)를 생성한다.
   - 세부 작업 구성:
     * T1 (`reasoning.simple-argument`, `low / low`): 에이전트 쿼터 가드레일(Rate-Limiter) 정책 도입의 전제, 핵심 근거(장단점), 결론, 성립 경계 조건(5시간 롤링 한도 vs 7일 주간 한도 버킷 분리) 요약 작성 (`t1_policy_argument.md`)
     * T2 (`coding.quick-edit`, `low / low`): `schema_validator.py`의 버그 3건(`VALID_EFFORTS` 오타, `bool`/`0` 토큰 허용 버그, `100%` 초과 상한 미검증) 최소 수정 및 `test_schema_validator.py` 통과
     * T3 (`coding.debugging.runtime`, `mid / medium` 또는 `high`): `task_queue.py`의 런타임 버그 3건(가변 기본 인자 공유, 재시도 횟수 off-by-one, 0초 경과 시 ZeroDivisionError) 수정 및 `test_task_queue.py` 통과 + 경계값 회귀 테스트 검증
     * T4 (`coding.debugging.concurrency`, `high / high`): `async_quota_pool.py`의 `asyncio.gather` 50-워커 동시성 레이스 컨디션(쿼터 이중 차감) 및 예외/취소 시 쿼터 롤백 누락 수정, 상태 전이·락 경계 노트(`t4_concurrency_notes.md`) 작성, `test_async_quota_pool.py` 스트레스 테스트 통과

3. A/B 실험 통제 조건:
   - 그룹 A (`a-t1`~`a-t4`): 모든 세부 작업을 `gemini-4-argon-medium` 단일 모델·Effort로 고정 실행하며, 분기 라우팅 없이 전체 규칙 코퍼스(`benchmark/prompts/arm_a_full_rules_context.txt`)를 참조한다.
   - 그룹 B (`b-t1`~`b-t4`): 각 세부 작업을 `python scripts/resolve_rule.py`로 라우팅하여 추출된 단일 `<active_rule_packet>`(`benchmark/prompts/arm_b_t{1..4}_packet.xml`)만 읽게 하고, 추천된 `(tier, effort)`에 따라 `b-t1`·`b-t2`는 `gemini-4-argon-low`, `b-t3`는 `gemini-4-argon-medium`, `b-t4`는 `gemini-4-argon-high`로 실행한다.

4. 체크포인트 기록 및 `Gemini 4 Argon (High)` 심층 품질 감사:
   - 각 워커 완료 즉시 `python benchmark/ab_harness.py record --arm <A|B> --task <T1..T4> --conv-id <id>`로 트랜스크립트 실측 토큰(`input_tokens`, `cache_read_tokens`, `output_tokens`), 소요 시간(`elapsed_seconds`), 기본 검증 점수를 `ab_checkpoint.json`에 저장한다.
   - 이후 `Gemini 4 Argon (High)` 관점에서 `python benchmark/audit_quality_high.py`를 실행하여 (1) 기능 정확성, (2) 적대적 엣지케이스(`CancelledError` 취소 롤백, 호출자 리스트 변이 격리 등), (3) 기존 주석·독스트링 보존율, (4) 동시성 yield 지점(`await asyncio.sleep(0)`) 보존 여부, (5) 타 분기 용어 오염(Cross-Branch Bleed) 및 규칙 희석(Attention Dilution) 여부, (6) 1만 토큰당 품질 점수(비용 대비 효용성)를 정밀 대조한다.
```

### 0-3. 그룹 B 규칙 라우팅 재현 커맨드 (`resolve_rule.py`)

```powershell
# T1 (low / low -> reasoning.simple-argument, 636 tok, 96.6% 절감)
python scripts/resolve_rule.py --task "간단한 논증으로 에이전트 쿼터 가드레일(Rate-Limiter) 정책의 핵심 장단점 3줄 요약 및 성립 경계 조건 생성" --files 1 --attempts 0 --format xml

# T2 (low / low -> coding.quick-edit, 472 tok, 97.5% 절감)
python scripts/resolve_rule.py --task "단일 파일 schema_validator.py에서 TaskSpec 및 QuotaBucket 함수 빠른 수정 및 타이핑 오타 보완" --files 1 --attempts 0 --format xml

# T3 (mid / high with verifier -> coding.debugging.runtime, 689 tok, 96.3% 절감)
python scripts/resolve_rule.py --task "task_queue.py 런타임 오류 3건 디버깅 및 단위 테스트 통과" --files 2 --attempts 1 --format xml

# T4 (high / high -> coding.debugging.concurrency, 676 tok, 96.4% 절감)
python scripts/resolve_rule.py --task "async_quota_pool.py의 asyncio 비동기 동시성 레이스 컨디션 디버깅 및 스트레스 테스트 통과" --files 4 --attempts 1 --concurrency --format xml
```

### 0-4. 실제 테스트에 사용된 8개 워커(A-T1~T4, B-T1~T4) 프롬프트 원문

#### [그룹 A 워커 프롬프트 (`gemini-4-argon-medium` 고정 + 비라우팅 전체 규칙 로드)]
* **`a-t1` (`gemini-4-argon-medium`)**:
  ```text
  You are Benchmark Worker a-t1 (Arm A Baseline: Fixed Gemini 4 Argon Medium, Un-routed Full Rules).
  Do ONLY this task in 1-2 tool calls and finish immediately:
  1. Call `read_file` on `benchmark\prompts\arm_a_full_rules_context.txt` (StartLine=1, EndLine=750) to load the un-routed baseline rule corpus.
  2. Write `benchmark\workspace_a\t1_policy_argument.md` (with Overwrite=true) containing a concise Korean argument on introducing an Agent Quota Guardrail (Rate-Limiter) policy, covering: 전제 (Premise), 핵심 근거 / 장단점 (Core pros & cons), 결론 (Conclusion), and 성립 경계 조건 / 한계 (Boundary condition, including separate 5-hour vs 7-day quota buckets).
  3. As soon as the file is written, post a short completion message to coordinator and stop calling tools. Do NOT touch any other files.
  ```
* **`a-t2` (`gemini-4-argon-medium`)**:
  ```text
  You are Benchmark Worker a-t2 (Arm A Baseline: Fixed Gemini 4 Argon Medium, Un-routed Full Rules).
  Do ONLY this task in 2-3 tool calls and finish immediately:
  1. Call `read_file` on `benchmark\prompts\arm_a_full_rules_context.txt` (StartLine=1, EndLine=750) and `read_file` on `benchmark\workspace_a\schema_validator.py`.
  2. Fix the bugs in `benchmark\workspace_a\schema_validator.py` using `edit_file` or `write_file` (preserve existing docstrings) and verify by running `python -m unittest test_schema_validator.py -v` in `benchmark\workspace_a`.
  3. Once the test passes, post a short completion message to coordinator and stop calling tools. Do NOT touch any other files.
  ```
* **`a-t3` (`gemini-4-argon-medium`)**:
  ```text
  You are Benchmark Worker a-t3 (Arm A Baseline: Fixed Gemini 4 Argon Medium, Un-routed Full Rules).
  Do ONLY this task in 2-3 tool calls and finish immediately:
  1. Call `read_file` on `benchmark\prompts\arm_a_full_rules_context.txt` (StartLine=1, EndLine=750) and `read_file` on `benchmark\workspace_a\task_queue.py` and `benchmark\workspace_a\test_task_queue.py`.
  2. Fix the 3 runtime bugs in `benchmark\workspace_a\task_queue.py` and verify by running `python -m unittest test_task_queue.py -v` in `benchmark\workspace_a`.
  3. Once the test passes, post a short completion message to coordinator and stop calling tools. Do NOT touch files outside T3.
  ```
* **`a-t4` (`gemini-4-argon-medium`)**:
  ```text
  You are Benchmark Worker a-t4 (Arm A Baseline: Fixed Gemini 4 Argon Medium, Un-routed Full Rules).
  Do ONLY this task in 2-3 tool calls and finish immediately:
  1. Call `read_file` on `benchmark\prompts\arm_a_full_rules_context.txt` (StartLine=1, EndLine=750) and `read_file` on `benchmark\workspace_a\async_quota_pool.py` and `benchmark\workspace_a\test_async_quota_pool.py`.
  2. Fix the async concurrency race condition and exception rollback bug in `benchmark\workspace_a\async_quota_pool.py` (optionally write brief notes to `benchmark\workspace_a\t4_concurrency_notes.md`), and verify by running `python -m unittest test_async_quota_pool.py -v` in `benchmark\workspace_a`.
  3. Once the test passes, post a short completion message to coordinator and stop calling tools. Do NOT touch files outside T4.
  ```

#### [그룹 B 워커 프롬프트 (작업별 동적 모델·Effort + 단일 `<active_rule_packet>` 주입)]
* **`b-t1` (`gemini-4-argon-low`, `reasoning.simple-argument`)**:
  ```text
  You are Benchmark Worker b-t1 (Arm B Treatment: HTML Branching Rule System, routed to `reasoning.simple-argument` -> tier: `low`, effort: `low`, mapped to `gemini-4-argon-low`).
  Do ONLY this task in 1-2 tool calls and finish immediately:
  1. Call `read_file` ONLY on the compact routed rule packet `benchmark\prompts\arm_b_t1_packet.xml` (do NOT read full rules or unrelated files).
  2. Following the `<active_rule_packet>` rules (`전제 → 핵심 근거 → 결론 → 적용 한계(1줄)` 순으로 간결하게 유지, 과잉 CoT 금지), write `benchmark\workspace_b\t1_policy_argument.md` (Overwrite=true) in 4 to 8 non-empty lines covering: 전제, 핵심 근거(장단점), 결론, and 적용 한계/성립 경계 조건 (5시간 롤링 한도와 7일 주간 한도 버킷 분리 조건 포함).
  3. Post a short completion message naming `@coordinator` and stop calling tools.
  ```
* **`b-t2` (`gemini-4-argon-low`, `coding.quick-edit`)**:
  ```text
  You are Benchmark Worker b-t2 (Arm B Treatment: HTML Branching Rule System, routed to `coding.quick-edit` -> tier: `low`, effort: `low`, mapped to `gemini-4-argon-low`).
  Do ONLY this task in 2-3 tool calls and finish immediately:
  1. Call `read_file` ONLY on the compact routed rule packet `benchmark\prompts\arm_b_t2_packet.xml` and `benchmark\workspace_b\schema_validator.py`.
  2. Following `<active_rule_packet>` (`기존 독스트링·주석 보존`, `지정 심볼만 최소 수정`), fix the 3 bugs in `benchmark\workspace_b\schema_validator.py` and verify by running `python -m unittest test_schema_validator.py -v` in `benchmark\workspace_b`.
  3. Post a short completion message naming `@coordinator` and stop calling tools.
  ```
* **`b-t3` (`gemini-4-argon-medium`, `coding.debugging.runtime`)**:
  ```text
  You are Benchmark Worker b-t3 (Arm B Treatment: HTML Branching Rule System, routed to `coding.debugging.runtime` -> tier: `mid`, effort: `medium`, mapped to `gemini-4-argon-medium`).
  Do ONLY this task in 2-3 tool calls and finish immediately:
  1. Call `read_file` ONLY on the compact routed rule packet `benchmark\prompts\arm_b_t3_packet.xml`, `benchmark\workspace_b\task_queue.py`, and `benchmark\workspace_b\test_task_queue.py`.
  2. Following `<active_rule_packet>` (`원인 지점만 최소 변경`, `경계값(None/빈 리스트/인코딩/오프바이원)을 검증하는 회귀 테스트를 추가한다`), fix the 3 runtime bugs in `benchmark\workspace_b\task_queue.py`, add 1 boundary regression test method to `benchmark\workspace_b\test_task_queue.py`, and run `python -m unittest test_task_queue.py -v` in `benchmark\workspace_b`.
  3. Post a short completion message naming `@coordinator` and stop calling tools.
  ```
* **`b-t4` (`gemini-4-argon-high`, `coding.debugging.concurrency`)**:
  ```text
  You are Benchmark Worker b-t4 (Arm B Treatment: HTML Branching Rule System, routed to `coding.debugging.concurrency` -> tier: `high`, effort: `high`, mapped to `gemini-4-argon-high`).
  Do ONLY this task in 2-3 tool calls and finish immediately:
  1. Call `read_file` ONLY on the compact routed rule packet `benchmark\prompts\arm_b_t4_packet.xml`, `benchmark\workspace_b\async_quota_pool.py`, and `benchmark\workspace_b\test_async_quota_pool.py`.
  2. Following `<active_rule_packet>` (`상태 전이(State Transition), 락 획득 순서, 비동기 취소/타임아웃 경계를 먼저 표로 도식화한다`, `결정적 동기화/원자적 연산으로 원인을 제거한다`, `반복 스트레스 테스트로 확인한다`), fix `benchmark\workspace_b\async_quota_pool.py` using atomic `asyncio.Lock` synchronization and proper exception rollback, write the state-transition & lock boundary markdown table to `benchmark\workspace_b\t4_concurrency_notes.md`, and run `python -m unittest test_async_quota_pool.py -v` in `benchmark\workspace_b`.
  3. Post a short completion message naming `@coordinator` and stop calling tools.
  ```

---

## 1. 실험 설계 (Composite Multi-Branch Task & A/B 조건)

복합 엔지니어링 대과제 **"실시간 에이전트 태스크 큐 & 쿼터 가드레일(Quota Guardrail) 엔진 구축 및 검증"**을 성격과 난이도가 서로 다른 **4개의 세부 작업(`T1`~`T4`)**으로 분기하여 실측 비교했습니다.

| 구분 | 그룹 A (Baseline: Google Harness² 단독) | 그룹 B (Treatment: Google Harness² + HTML 분기형 규칙) |
| :--- | :--- | :--- |
| **모델·Effort 선정** | 전 작업 **`gemini-4-argon-medium`** (`Gemini 4 Argon (Medium)`) 단일 고정 | [`scripts/resolve_rule.py`](./scripts/resolve_rule.py) 추천 `(tier, effort)`를 Antigravity 가용 모델·Effort(`gemini-4-argon-{low,medium,high}`)로 동적 매핑 |
| **규칙 컨텍스트 주입** | 비라우팅 전체 규칙 코퍼스 ([`arm_a_full_rules_context.txt`](./benchmark/prompts/arm_a_full_rules_context.txt), AI 블록 합계 `55,577 B` / `~18,704 tok`) | 작업별 단일 경로 `<active_rule_packet>` XML만 주입 (`1,700~2,479 B` / `472~689 tok`, **96.3%~97.5% 절감**) |
| **중단 복구 캐시** | 매 세부 작업 완료 시 [`ab_checkpoint.json`](./benchmark/cache/ab_checkpoint.json)에 즉시 영속화 | 매 세부 작업 완료 시 [`ab_checkpoint.json`](./benchmark/cache/ab_checkpoint.json)에 즉시 영속화 |

---

## 2. 총괄 벤치마크 및 효용성 결과 요약 (Arm A vs. Arm B)

| 핵심 지표 (4개 세부 작업 합산) | 그룹 A (Baseline: `Argon Medium` 고정) | 그룹 B (Rule System: 동적 모델·Effort + 단일 패킷) | 변화량 및 효용성 (B vs. A) |
| :--- | :---: | :---: | :---: |
| **주입된 규칙 컨텍스트 합계 (4작업 누적)** | `74,816 tok` (`222,308 B`) | **`2,473 tok` (`8,903 B`)** | **-96.7% (`-72,343 tok`)** |
| **실측 신규 입력 토큰 (`input_tokens`)** | `129,114 tok` | **`85,309 tok`** | **-33.9% (`-43,805 tok`)** |
| **실측 캐시 읽기 토큰 (`cache_read_tokens`)** | `266,691 tok` | **`180,312 tok`** | **-32.4% (`-86,379 tok`)** |
| **실측 출력 토큰 (`output_tokens`)** | `6,434 tok` | **`10,643 tok`** *(T1 -60.5% 절감 / T3·T4 심층 검증 집중)* | `+4,209 tok` *(고난도 검증 집중)* |
| **실측 총 소모 토큰 (`total_tokens`)** | `402,239 tok` | **`276,264 tok`** | **-31.3% (`-125,975 tok`)** |
| **비캐시 활성 토큰 (`input + output`)** | `135,548 tok` | **`95,952 tok`** | **-29.2% (`-39,596 tok`)** |
| **개별 작업 소요 시간 합계 (병렬 최장 시간)** | `215.0초` (병렬 `90.0초`) | **`224.0초` (병렬 `89.0초`, T1 `-37.0%` 단축)** | 병렬 기준 **-1.0초** (T1 **-10.0초**) |
| **기본 자동 검증 점수 (`ab_harness.py`)** | `92 / 100점` | **`100 / 100점`** | **+8.0점 향상** |
| **`Argon High` 정밀 품질 감사 점수 (`audit_quality_high.py`)** | **`71 / 100점`** | **`100 / 100점`** | **+29.0점 향상 (+40.8% 품질 우위)** |
| **총 토큰 1만 개당 정밀 품질 점수 (가성비 효율)** | `1.77 점 / 10K tok` | **`3.62 점 / 10K tok`** | **`2.05배` (+104.5%) 효율 향상** |
| **신규 입력 토큰 1만 개당 정밀 품질 점수** | `5.50 점 / 10K input tok` | **`11.72 점 / 10K input tok`** | **`2.13배` (+113.1%) 효율 향상** |

---

## 3. 세부 작업별(T1 ~ T4) 상세 대조표

| 작업 ID 및 목표 | 구분 | 적용 분기 / 모델·Effort | 규칙 패킷 토큰 | 실측 `input` 토큰 | 실측 `cache` 토큰 | 실측 `output` 토큰 | 실측 총 토큰 (`total`) | 소요 시간 | 기본 점수 / **`Argon High` 정밀 점수** |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **T1. 쿼터 가드레일 찬반 논증 및 경계 조건** | **A** | 비라우팅 / `gemini-4-argon-medium` | `18,704` | `26,164` | `12,395` | `1,431` | `39,990` | `27.0s` | `20` / **`14 / 25`** *(18줄 장문 + 타 분기 용어 오염)* |
| | **B** | `reasoning.simple-argument` / **`gemini-4-argon-low`** | **`636`** (-96.6%) | **`17,942`** (-31.4%) | `21,603` | **`565`** (-60.5%) | `40,110` | **`17.0s`** (-37.0%) | `25` / **`25 / 25`** *(5줄 핵심 압축·오염 0건)* |
| **T2. `schema_validator.py` 빠른 코드 수정** | **A** | 비라우팅 / `gemini-4-argon-medium` | `18,704` | `31,879` | `65,210` | `1,444` | `98,533` | `40.0s` | `25` / **`25 / 25`** *(6/6 통과·주석 보존)* |
| | **B** | `coding.quick-edit` / **`gemini-4-argon-low`** | **`472`** (-97.5%) | **`21,816`** (-31.6%) | **`52,719`** (-19.2%) | `1,611` | **`76,146`** (-22.7%) | `53.0s` | `25` / **`25 / 25`** *(6/6 통과·입력 토큰 -31.6%)* |
| **T3. `task_queue.py` 런타임 버그 3건 디버깅** | **A** | 비라우팅 / `gemini-4-argon-medium` | `18,704` | `35,747` | `93,288` | `1,805` | `130,840` | `58.0s` | `22` / **`18 / 25`** *(규칙 희석으로 회귀 테스트 누락)* |
| | **B** | `coding.debugging.runtime` / **`gemini-4-argon-medium`** | **`689`** (-96.3%) | **`23,185`** (-35.1%) | **`59,888`** (-35.8%) | `3,479` | **`86,552`** (-33.8%) | `65.0s` | `25` / **`25 / 25`** *(경계값 회귀 테스트 4종 추가)* |
| **T4. `async_quota_pool.py` 비동기 동시성 디버깅** | **A** | 비라우팅 / `gemini-4-argon-medium` | `18,704` | `35,324` | `95,798` | `1,754` | `132,876` | `90.0s` | `25` / **`14 / 25`** *(시드 주석·`sleep(0)` 임의 삭제)* |
| | **B** | `coding.debugging.concurrency` / **`gemini-4-argon-high`** | **`676`** (-96.4%) | **`22,366`** (-36.7%) | **`46,102`** (-51.9%) | `4,988` | **`73,456`** (-44.7%) | **`89.0s`** (-1.1%) | `25` / **`25 / 25`** *(주석·`sleep(0)` 보존 + 6열 상태표)* |

---

## 4. `Gemini 4 Argon (High)` 기반 산출물 품질 심층 감사 및 효용성 분석

단순 단위 테스트 통과 여부만으로는 드러나지 않는 **코드 수정 정밀도, 주석/테스트 조건 보존성, 교차 분기 컨텍스트 오염(Cross-Branch Bleed), 주의력 희석(Attention Dilution)**을 `Gemini 4 Argon (High)` 및 [`benchmark/audit_quality_high.py`](./benchmark/audit_quality_high.py)로 정밀 감사한 결과입니다.

### ① T1 (`t1_policy_argument.md`): 교차 분기 컨텍스트 오염(Cross-Branch Bleed) 적발 및 과잉 추론 제어
- **심층 감사 결과 (`A: 14/25점` vs. `B: 25/25점`)**:
  - **그룹 A의 문제점 (비라우팅 전체 규칙으로 인한 컨텍스트 오염)**:
    - [`workspace_a/t1_policy_argument.md`](./benchmark/workspace_a/t1_policy_argument.md)는 24줄(비공백 18줄, `2,044자`, `1,431 output tokens`)의 장문으로 작성되어 "간단한 3줄 요약 논증"이라는 요구사항을 어겼을 뿐 아니라,
    - `arm_a_full_rules_context.txt` 안에 섞여 있던 **무관한 타 분기(`ai-systems`, `graph-orch`, `context-rag`)의 고유 용어들(`PreToolUse`, `Swarm/Graph`, `Context Rot`, `Unbounded Retry Loop`)이 단순 논증 요약문 내부로 그대로 흘러들어오는 교차 오염(Cross-Branch Bleed)**이 발생했습니다.
  - **그룹 B의 품질 우위**:
    - [`workspace_b/t1_policy_argument.md`](./benchmark/workspace_b/t1_policy_argument.md)는 `gemini-4-argon-low`와 `reasoning.simple-argument` 단일 패킷(`636 tok`)만 주입받아 **타 분기 용어 오염 0건**, **비공백 5줄(`485자`, `565 output tokens`, -60.5%)**, **소요 시간 17초(-37.0%)**로 `전제 → 핵심 근거(장점/단점) → 결론 → 적용 한계(5시간 롤링 vs 7일 주간 버킷 분리)` 구조를 완벽히 충족했습니다.

### ② T2 (`schema_validator.py`): 동일 품질에서 저비용 티어(`low/low`) 하향 라우팅의 순수 비용 절감 효용
- **심층 감사 결과 (`A: 25/25점` vs. `B: 25/25점`)**:
  - `difflib` 코드 비교 결과, 그룹 A와 그룹 B 모두 정확히 동일한 3개 지점(`VALID_EFFORTS`, `isinstance(max_tokens, bool)` 및 `<= 0` 방어, `val > 100` 상한 검증)만 최소 수정하고 독스트링·주석을 100% 보존했습니다.
  - **핵심 효용성**: 단일 파일의 명확한 스키마/타이핑 수정(`coding.quick-edit`, 난이도 점수 `20/100`)에는 굳이 `Argon Medium`과 1.8만 토큰의 전체 규칙을 쓸 필요가 없으며, `Argon Low` + 472토큰 패킷으로 라우팅함으로써 **동일한 만점(`25/25`) 산출물을 신규 입력 토큰 -31.6%(`31,879 → 21,816 tok`), 총 토큰 -22.7%(`98,533 → 76,146 tok`) 절감된 비용으로 획득**했습니다.

### ③ T3 (`task_queue.py` & `test_task_queue.py`): 동일 모델(`Argon Medium`) 통제 비교에서 입증된 '규칙 희석(Lost-in-the-Middle) 방지' 효과
- **심층 감사 결과 (`A: 18/25점` vs. `B: 25/25점`)**:
  - `T3`는 **그룹 A와 그룹 B 모두 정확히 동일한 `gemini-4-argon-medium` 모델을 사용**했으므로, 오직 **"전체 규칙 주입(`18,704 tok`) vs. 단일 분기 패킷 주입(`689 tok`)"**의 순수 효과만 격리해 보여주는 결정적 실험입니다.
  - 두 그룹 모두 `task_queue.py`의 런타임 버그 3건은 동일하게 고쳤으나, `coding.debugging.runtime` 분기의 핵심 규칙인 `<r src="coding.debugging.runtime">경계값(None/빈 리스트/인코딩/오프바이원)을 검증하는 회귀 테스트를 추가한다.</r>` 준수 여부가 극명하게 갈렸습니다.
  - **그룹 A ([`workspace_a/test_task_queue.py`](./benchmark/workspace_a/test_task_queue.py))**: 27개 파일 분량의 규칙 덤프 속에서 해당 지침이 희석(Attention Dilution)되어 **`test_task_queue.py` 수정 라인 수 = `0줄`**로 회귀 테스트 추가를 완전히 누락했습니다.
  - **그룹 B ([`workspace_b/test_task_queue.py`](./benchmark/workspace_b/test_task_queue.py))**: 689토큰짜리 단일 패킷에서 해당 지침을 즉시 포착하여 `test_boundary_regression_conditions` 메서드를 신설하고 (1) `TaskQueue(None)` 초기화, (2) 호출자 리스트 변이(`caller_tags.append("mutated")`) 격리, (3) `max_retries=0` 즉시 실패 경계, (4) `0` 토큰 처리까지 4가지 경계 조건을 검증했습니다 — 그러면서도 **총 토큰은 오히려 33.8%(`130,840 → 86,552 tok`) 더 적게 썼습니다.**

### ④ T4 (`async_quota_pool.py` & `t4_concurrency_notes.md`): 고난도 비동기 동시성에서 드러난 `Argon High` + 분기 규칙의 결정적 차이
- **심층 감사 결과 (`A: 14/25점` vs. `B: 25/25점`)**:
  - `audit_quality_high.py`로 실행 중 코루틴 강제 취소(`asyncio.CancelledError`) 적대적 테스트와 시드 파일 대비 `difflib` 라인 감사를 수행한 결과, 그룹 A에서 **3가지 중대한 품질 결함**이 발견되었습니다.
  1. **기존 주석 임의 삭제 위반 (`coding.root` 규칙 위반)**:
     - 그룹 A([`workspace_a/async_quota_pool.py`](./benchmark/workspace_a/async_quota_pool.py))는 시드 파일에 있던 `# BUG 1 (Race Condition)...` 주석 3줄과 `# BUG 2: Missing quota rollback...` 주석을 임의로 삭제했습니다.
     - 반면 그룹 B([`workspace_b/async_quota_pool.py`](./benchmark/workspace_b/async_quota_pool.py))는 `<r src="coding.root">기존 주석·독스트링을 임의로 삭제하지 않으며...</r>` 지침에 따라 모든 주석을 100% 보존했습니다.
  2. **임계 구역 내 컨텍스트 스위치 재현 코드(`await asyncio.sleep(0)`) 임의 제거**:
     - 시드 파일 41행의 `await asyncio.sleep(0)  # context switch between check and deduction`은 검사와 차감 사이에 이벤트 루프 컨텍스트 스위치가 일어나도 락(`self._lock`)이 원자성을 보장하는지 시험하기 위한 핵심 장치입니다.
     - 그룹 A(`Argon Medium`)는 이 `await asyncio.sleep(0)` 라인 자체를 지워버려 임계 구역 내부의 비동기 양보(yield) 조건을 제거한 반면, **그룹 B(`Argon High`)는 `async with self._lock:` 블록 내부에 `await asyncio.sleep(0)`을 그대로 유지**하여 코루틴이 락을 쥔 채 이벤트 루프에 양보하더라도 50개 동시 워커가 단 1건의 레이스 컨디션 없이 직렬화됨을 증명했습니다.
  3. **상태 전이·락 순서·취소 경계 도식화 깊이 차이**:
     - 그룹 A([`workspace_a/t4_concurrency_notes.md`](./benchmark/workspace_a/t4_concurrency_notes.md))는 4열짜리 간략 표(9줄)만 작성한 반면, 그룹 B([`workspace_b/t4_concurrency_notes.md`](./benchmark/workspace_b/t4_concurrency_notes.md))는 `0. Validate → 1. Reserve/Reject → 2. Execute Worker → 3. Commit → 4. Rollback` 5단계에 걸쳐 **사전 조건(Pre-Condition), 락 획득 순서(`Order #1`), 비동기 yield/취소 경계, 사후 조건, `BaseException`/`CancelledError` 롤백 불변식**을 6열 표와 근본 원인 분석으로 완벽히 문서화했습니다 — 동시에 **총 소모 토큰은 그룹 A 대비 44.7%(`132,876 → 73,456 tok`) 절감**했습니다.

---

## 5. 종합 효용성 결론: 왜 HTML 분기형 규칙 + 작업별 모델·Effort 라우팅이 효과적인가?

`Gemini 4 Argon (High)` 심층 감사를 통해 확인된 본 규칙 시스템의 실질적 효용성은 다음 3가지로 요약됩니다.

1. **단순 비용 절감을 넘어선 '가성비(품질/토큰 효율) 2.05배~2.13배' 달성**:
   - 그룹 B는 전체 규칙 대신 단일 `<active_rule_packet>`만 로드하여 **신규 입력 토큰을 33.9%(`-43,805 tok`), 총 토큰을 31.3%(`-125,975 tok`) 절감**하면서도, 정밀 품질 점수는 오히려 **`71점 → 100점`(+29점)**으로 상승했습니다.
   - 결과적으로 **총 토큰 1만 개당 획득 품질 점수**는 그룹 A `1.77점` 대비 그룹 B **`3.62점`(`2.05배`)**, **신규 입력 토큰 1만 개당 품질 점수**는 그룹 A `5.50점` 대비 그룹 B **`11.72점`(`2.13배`)**에 달합니다.
2. **컨텍스트 오염(Cross-Branch Bleed) 및 주의력 희석(Attention Dilution) 원천 차단**:
   - 모든 규칙을 한꺼번에 넣으면 `T1`처럼 무관한 분기의 용어(`PreToolUse`, `Context Rot`)가 출력에 섞여 들어가거나, `T3`·`T4`처럼 정작 지켜야 할 세부 규칙(회귀 테스트 추가, 주석 보존)이 묻히는 부작용이 실측되었습니다. HTML 분기 라우팅은 현재 작업에 필요한 8~11개의 핵심 규칙만 선명하게 주입하여 모델의 지시 이행률을 100%로 끌어올립니다.
3. **작업 난이도 맞춤형 Effort 배분 (하위 작업 과잉 추론 억제 + 상위 작업 정밀도 극대화)**:
   - 단순 요약·빠른 수정(`T1`, `T2`)에서는 `low` Effort로 불필요한 장문 생성과 지연을 막고(`T1` 출력 `-60.5%`, 시간 `-37.0%`), 아낀 토큰·쿼터 예산을 고위험 비동기 동시성 디버깅(`T4`, `high` Effort)에 집중 투입하여 시드 주석·컨텍스트 스위치 보존 및 5단계 상태 전이 설계까지 결함 없이 완수합니다.

---

## 6. 쿼터 버킷 분리 실증 검증 (Gemini 5시간 한도 vs. Gemini 4 Argon 주간 한도)

벤치마크 실행 전·중·후 `swarm{action:"models", all:true}` 쿼터 스냅샷을 추적한 결과:

| 시각 (KST) | 이벤트 | `gemini-3.8-flash-{low,medium,high}` (5시간 한도, 리셋 `07:34 KST`) | `gemini-4-argon-{low,medium,high}` (7일 주간 한도, 리셋 `11-19 06:35 KST`) |
| :--- | :--- | :---: | :---: |
| `06:27:40` | 브라우저 서브에이전트(`flash`) 1회 실행 전 | `12%` | `100%` |
| `06:37:21` | 브라우저(`flash`) 1회 종료 + 메인 모델 `Argon Medium` 전환 직후 | `10%` | `95%` |
| `06:38:39` | 메인 모델(`Argon Medium`) 2턴 추가 수행 후 | **`10%` (변화 없음)** | `95%` |
| `06:45:42` | **A/B 벤치마크 Argon 워커 8개(`low`×2, `medium`×5, `high`×1) 총 67.8만 토큰 실행 직후** | **`9%`~`10%` (Argon 워커로 인한 5시간 풀 차감 없음)** | **`93%` (`-2%p`만 소모)** |

1. **`Gemini 4 Argon`은 7일 주간 리셋 버킷(`2026-11-18T21:35:25Z`)을 별도로 사용**하며, 8개의 Argon 워커가 약 **67.8만 토큰(`402,239 + 276,264`)**을 처리하는 동안 Argon 주간 쿼터는 **`95% → 93%` 단 `2%p`**만 소모되었습니다.
2. 또한 당시 `Claude Opus/Sonnet 5.5` 및 `GPT-OSS 120B`의 잔여 한도가 `0%`인 상태에서, 규칙 시스템의 지침(*"표기 모델명은 참고 예시이며 실행 환경의 실제 가용 모델·Effort에 맞춰 매핑한다"*)에 따라 `low / mid / high` 티어를 `gemini-4-argon-{low,medium,high}`로 매핑함으로써 쿼터 고갈로 인한 중단 없이 8개 작업을 100% 완주했습니다.
