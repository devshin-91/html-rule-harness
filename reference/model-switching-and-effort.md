# Effort Scaling vs. Model Switching Empirical Guide (`reference/model-switching-and-effort.md`)

각 작업(코딩, 디버깅, RAG/리서치, 논증, 멀티에이전트)에서 **동일 모델의 추론 노력(`effort`/`thinking_level`)만 올릴지, 아니면 모델 자체를 변경(상·하향 또는 특화 프로파일 전환)할지** 결정하기 위해 GitHub/오픈소스 라우터, 모델 벤더 공식 문서, Liner Scholar 학술 논문을 조사·반영한 레퍼런스입니다.

---

## 1. 모델 벤더 공식 제어 파라미터 & 전환 기준 (Web Research)

| 벤더 | 공식 Effort 제어 파라미터 | 지원 단계 | 모델 변경(Switch) 기준 |
|---|---|---|---|
| **OpenAI** | `reasoning.effort` / `reasoning_effort` | `none`, `minimal`, `low`, `medium`, `high`, `xhigh` | 구조화 추출·단순 편집은 비추론/mini; 일반 로직은 reasoning `low/medium`; 고모호·아키텍처·분산 루프는 frontier + `high/xhigh` 전환 |
| **Anthropic** | `output_config.effort` + `thinking:{type:"adaptive"}` | `low`, `medium`, `high`, `xhigh`, `max` | 대량·요약(`Haiku`) → 코딩·디버깅(`Sonnet`) → Sonnet `high/xhigh` 초과 시 **Opus `medium`** 전환이 반복 루프보다 효율적 |
| **Google Gemini** | `generation_config.thinking_level` | `minimal`, `low`, `medium`, `high` | 멀티모달·1M 대용량 컨텍스트 수집은 `Flash`; 상충 근거 대조·심층 코드/추론은 `Pro` 전환 |

---

## 2. 오픈소스 라우터 & Test-Time Compute 최적화 패턴 (GitHub & Web)

1. **`lm-sys/RouteLLM` (`arXiv:2406.18665`) & `vllm-project/semantic-router`**:
   - 단일 저비용 분류기로 복잡도·의도·안전 경계를 1차 분기하되, 정적 라우팅 실패 시 테스트/검증기 게이트와 결합해 상위 모델로 캐스케이드(Cascade) 전환.
2. **Test-Time Scaling 전략 분기 (`Snell et al., 2024`, `arXiv:2408.03314`)**:
   - 작은 모델이 0%가 아닌 기반 성공률을 가지는 **검증 가능 문제**에서는 Test-Time Compute(순차 수정/탐색)가 14× 큰 모델에 필적하나, 난이도가 기반 모델 역량을 넘으면 즉시 파라미터 스케일(큰 모델)로 전환해야 함.

---

## 3. Liner Scholar 실증 논문 및 작업별 전환 임계치 (6차 세션)

> 탐색 스레드: *Agent Scaling* (Liner Scholar, 30편 큐레이션 테이블 *Scaling Test-Time Compute: Efficiency, Performance Ceilings, and Optimal Strategies*)

### A. Effort 상향이 효과적인 조건 (Keep Model, Raise Effort)
1. **외부 실행 검증기(테스트·컴파일러·샌드박스)가 있는 코딩/SWE**:
   - **Ma et al. (2025)** (`arXiv:2503.20522`): 실행 피드백 기반 동적 테스트타임 컴퓨트 할당으로 32B 모델이 SWE-bench Verified `46%`를 달성해 671B DeepSeek-R1/o1을 상회.
   - **Brown et al. (2024)** (*Large Language Monkeys*, `arXiv:2407.21787`) & **Ding & Zhang (2026)** (*SWE-Replay*, `arXiv:2601.22129`): 단위 테스트 검증기가 있으면 반복 탐색·접두사 재사용(`-17.4%` 비용)이 유효함.
   - **Li & Shi (2026)** (*Interaction Scaling*, `arXiv:2607.11598`): 순수 내부 사고만 늘리는 대신 환경/테스트 상호작용을 통해 정체 구간 돌파.

### B. Effort 상향이 실패하고 모델 전환(Model Switch)이 필수인 4대 천장
1. **Reasoning Floor (기반 역량 하한 천장)**:
   - **Wang et al. (2025)** (`arXiv:2504.14047`) & **Javanmard et al. (2025)** (`arXiv:2510.03605`): 필요한 추론 프리미티브·논리 규칙이 사전학습 역량에 없으면 추론 컴퓨트를 10배 늘려도 돌파 불가능하며 오히려 정확도가 하락함 → `architecture`, `concurrency`, `structured-argument`(반론/아첨 방어), `security`, `frontier-craft`는 **모델 자체 전환(`capacity-switch-sensitive`)** 필수.
2. **Modal Ceiling (검증기 부재 시 선택 상한)**:
   - **Bay & Yearick (2026)** (`arXiv:2606.28661`) & **Halder & Pehlevan (2025)** (`arXiv:2512.19905`): 테스트/오라클 검증기가 없는 과제에서는 추가 샘플링·추론이 수십 회 내에 모달 천장에 막혀 일관된 오답을 고착화함 → `--no-verifier` 조건에서는 1회 실패만으로도 Effort 재시도 대신 **즉시 상위 모델 전환(`switch_model_up`)**.
3. **T2MO 경제적 재시도 임계 & 과잉 탐욕 소비**:
   - **Manoharan et al. (2026)** (`arXiv:2608.08528`, T2MO) & **Fan et al. (2026)** (`arXiv:2608.07968`): 2회 이상 실패 또는 4개+ 파일 결합 시 누적 재시도·대기 비용이 상위 모델 단발 호출 비용을 초과함. 또한 **Wang et al. (2026)** (`arXiv:2610.02762`)은 6개 정적 라우터가 난이도 맹목으로 실패함을 보였고, **Shaikh (2026)** (`zenodo:21330788`)는 베이지안 단계별 동적 에스컬레이션의 우위를 입증함.
4. **RAG · 사실 조회의 검색/리랭킹 전환 법칙 (`grounding-over-thinking`)**:
   - **Apparaju & Gupta (2026)** (`arXiv:2603.14635`): BRIGHT 벤치마크 기준 **리랭커 모델 상향은 `+7.5 NDCG@10`**로 선형 이득을 주나, 쿼리 확장(`+1.1 NDCG@10`)과 생성기 thinking 토큰 증가는 거의 효과가 없음.
   - **Yue et al. (2024)** (`arXiv:2410.04343`) & **Zhou et al. (2026, AAAI)** & **Jin et al. (2025)** (`arXiv:2505.14733`): 사실 회상은 추론 토큰이 아닌 검색·파라미터/리랭커 배분이 핵심 → [`research/`](./rules/branches/research/index.html) 및 [`context-rag.html`](./rules/branches/ai-systems/context-rag.html)는 모호성 시 thinking 증가 대신 검색·리랭커 전환(`ground_before_think`)을 권고함.
5. **Overthinking Inversion (단순 과제 역전 방어)**:
   - **Zhou et al. (2026)** (`arXiv:2604.10739`), **Liu et al. (2025)** (`arXiv:2502.06703`), **Wu et al. (2024)** (`arXiv:2408.00724`): 단순 과제는 thinking 토큰 초과 시 기존 정답을 스스로 뒤집으므로 [`overthinking-guard-low`]로 방어.

---

## 4. 프로젝트 반영 요약

- [`rules/model-catalog.json`](../rules/model-catalog.json): 벤더별 API 제어 파라미터(`provider_controls`), 4대 적응 정책(`adaptation_policies`), 작업 특화 모델 전환 가이드(`workload_specialists`) 통합.
- [`scripts/resolve_rule.py`](../scripts/resolve_rule.py) & [`rules/assets/rule-ui.js`](../rules/assets/rule-ui.js): 작업 정책 + 외부 검증기(`--no-verifier` / UI 체크박스) 유무에 따라 **`keep_optimal` / `raise_effort` / `switch_model_up` / `ground_before_think`** 액션을 결정적으로 산출.
- [`rules/branches/meta/model-router-policy.html`](../rules/branches/meta/model-router-policy.html) 및 각 도메인 리프 노드에 `data-escalation-policy`·`data-workload` 속성 반영.
