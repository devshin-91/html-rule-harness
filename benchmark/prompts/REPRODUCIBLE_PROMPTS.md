# 재현 가능한 A/B 벤치마크 프롬프트 명세 (`REPRODUCIBLE_PROMPTS.md`)

본 문서는 [`benchmark/AB_BENCHMARK_REPORT.md`](../AB_BENCHMARK_REPORT.md)의 실험을 누구나 동일하게 재현할 수 있도록 정리한 **표준 마스터 프롬프트**와 **세부 워커 프롬프트(`a-t1`~`a-t4`, `b-t1`~`b-t4`)** 사본입니다.

---

## 1. 재현용 마스터 프롬프트 (Copy-Paste Master Prompt)

```markdown
현재 워크스페이스(`html-rule-harness`)에서 Google Harness² 단독 실행(그룹 A)과 Google Harness² + HTML 분기형 규칙 라우팅 시스템 적용(그룹 B)의 실증 A/B 벤치마크를 수행하라.

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
   - 각 워커 완료 즉시 `python benchmark/ab_harness.py record --arm <A|B> --task <T1..T4> --conv-id <id>`로 트랜스크립트 실측 토큰(`input_tokens`, `cache_read_tokens`, `output_tokens`), 소요 시간(`elapsed_seconds`), 루브릭 검증 점수(각 25점, 총 100점)를 `ab_checkpoint.json`에 저장한다.
   - 마지막으로 `python benchmark/ab_harness.py verify`와 상위 모델(`Gemini 4 Argon (High)`) 기반 정밀 품질 감사 스크립트 `python benchmark/audit_quality_high.py`를 실행하여, 그룹 A와 그룹 B의 소요 시간, 토큰 소모량, 실제 산출물 품질 차이(교차 분기 오염, 주의력 희석, 주석·yield 보존, 토큰당 품질 효율)를 표로 대조 보고한다.
```

---

## 2. CLI 초기화 및 자동 검증 커맨드

```powershell
# 1. 워크스페이스 A/B 시드 초기화 및 라우팅 패킷·체크포인트 생성
python benchmark/ab_harness.py init

# 2. 워커 실행 후 트랜스크립트 텔레메트리 및 점수 기록
python benchmark/ab_harness.py record --arm A --task T1 --conv-id <conv-id>
python benchmark/ab_harness.py record --arm B --task T1 --conv-id <conv-id>

# 3. 그룹 A vs 그룹 B 기본 100점 루브릭 및 단위/스트레스 테스트 일괄 검증
python benchmark/ab_harness.py verify

# 4. Gemini 4 Argon (High) 기준 6대 차원 정밀 품질 감사 및 토큰당 가성비 산출
python benchmark/audit_quality_high.py
```
