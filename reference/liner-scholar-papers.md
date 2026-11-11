# Liner Scholar Academic Paper References (`reference/liner-scholar-papers.md`)

**Liner Scholar** (`https://scholar.liner.com`) 학술 검색을 통해 단계별(Phase 1~6)로 조사·반영한 핵심 논문 목록입니다.

---

## A. Context Engineering & Progressive Disclosure (Query 1)

1. **Indexing the Unreadable: LLM-Native Recursive Construction and Search of Service Taxonomies**
   - **저자/연도**: Zheng et al. (2026) · `https://arxiv.org/abs/2605.29270`
   - **핵심 요약**: 계층적 분류 체계(taxonomy)를 쿼리 시점에 레이어별로 탐색하는 Progressive Disclosure(A2X)가 전체 컨텍스트 주입 대비 Hit Rate +6.2pt 향상 및 **프롬프트 토큰 비용 1/9 절감** 달성.
   - **반영**: `router.html` → `branches/<domain>/` 1단계씩 좁혀 들어가는 탐색 프로토콜.

2. **APDMem: Agent-Controlled Progressive Disclosure for Query-Adaptive Long-Term Memory**
   - **저자/연도**: Fu et al. (2026) · `https://arxiv.org/abs/2610.02472`
   - **핵심 요약**: 4계층 메모리 중 필요할 때만 하위 노드를 열람해 전체 문맥의 약 **8%**만 접근하면서 과제 해결.
   - **반영**: 활성 분기 패킷(`<active_rule_packet>`)이 전체 HTML 규칙 트리의 ~5% 내외만 반영하도록 설계.

3. **Is Progressive Disclosure All You Need for Long-Context Agents?**
   - **저자/연도**: He et al. (2026) · `https://arxiv.org/abs/2607.17598`
   - **핵심 요약**: 1단계 Progressive Disclosure는 다수 문서 스케일링에 결정적이나, 과도하게 깊은 다단계 라우팅은 정확도를 떨어뜨릴 수 있음("progressive disclosure buys context, not intelligence").
   - **반영**: HTML 분기 깊이를 최대 3단계(`Depth 0~3`)로 제한하는 권고치를 `validate_harness.py`에 추가하고, `resolve_rule.py`로 단일 XML 패킷으로 결정적 병합함.

4. **Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models (ACE)**
   - **저자/연도**: Zhang et al. (2025) · `https://arxiv.org/abs/2510.04618`
   - **핵심 요약**: 에이전트 컨텍스트를 구조적·점진적 플레이북으로 진화시켜 컨텍스트 붕괴(context collapse)를 방지.
   - **반영**: `library/EXPERIENCE.md`와 `Propose–Probe–Compose`의 점진적 분기 정제 규칙.

5. **기타 연관 조사 논문**
   - **Memory for Autonomous LLM Agents** — Du (2026), `https://arxiv.org/abs/2603.07670`
   - **A Survey of Context Engineering for LLMs** — Mei et al. (2025), `https://arxiv.org/abs/2507.13334`
   - **Context engineering frames prompt engineering within system level orchestration** — Kővári (2026), *Discover AI* (`https://link.springer.com/10.1007/s44163-026-02312-x`)

---

## B. Difficulty-Aware Model Routing, Cascades & Reasoning Effort (Query 2)

1. **A Unified Approach to Routing and Cascading for LLMs**
   - **저자/연도**: Dekoninck et al. (2024) · `https://arxiv.org/abs/2410.10347`
   - **핵심 요약**: 사전 라우팅(Routing)과 실패 시 상위 모델 승격(Cascading)을 결합한 **Cascade Routing**이 단독 기법보다 일관되게 우월함을 증명.
   - **반영**: 분기 기본 `data-tier` 선택 + `data-escalate-when` (2회 실패, 결합 파일 4+) 기반 상위 모델 자동 승격 구조.

2. **Scaling LLM Test-Time Compute Optimally**
   - **저자/연도**: Snell et al. (2024) · `https://arxiv.org/abs/2408.03314`
   - **핵심 요약**: 프롬프트 난이도에 따라 테스트 시점 연산량(compute)을 다르게 배분하면 모델 파라미터 확대보다 4배 이상 효율적일 수 있음.

3. **e1: Learning Adaptive Control of Reasoning Effort**
   - **저자/연도**: Kleinman et al. (2025) · `https://arxiv.org/abs/2510.27042`
   - **핵심 요약**: 난이도에 따라 연속적 Reasoning Effort를 제어해 정확도 유지/향상과 함께 CoT 토큰 2~3배 절감.
   - **반영**: 모델 티어(`low`/`mid`/`high`)와 별개로 각 HTML 분기 노드에 `data-effort` (`low`/`medium`/`high`)를 독립 권장 필드로 분리.

4. **RADAR: Reasoning-Ability and Difficulty-Aware Routing for Reasoning LLMs**
   - **저자/연도**: Fernandez et al. (2025) · `https://arxiv.org/abs/2509.25426`
   - **핵심 요약**: 문항반응이론(IRT)으로 질의 난이도와 모델-예산 역량을 추정해 8개 추론 벤치마크에서 기존 라우터 능가.

5. **기초 모델 라우팅·캐스케이드 논문**
   - **RouteLLM** — Ong et al. (2024), `https://arxiv.org/abs/2406.18665`
   - **FrugalGPT** — Chen et al. (2023), `https://arxiv.org/abs/2305.05176`
   - **Hybrid LLM** — Ding et al. (2024), `https://arxiv.org/abs/2404.14618`
   - **Learning How Hard to Think** — Damani et al. (2024), `https://arxiv.org/abs/2410.04707`
   - **BEST-Route** — Ding et al. (2025), `https://arxiv.org/abs/2506.22716`
   - **Adaptive Computation in the LLM Era (Survey)** — Cheung (2026), Cambridge University Press (`https://www.cambridge.org/engage/coe/article-details/6a2fa5614770e67d92f5bb0c`)

---

## C. Agent Orchestration, Loops & Graph Workflows (2차 Query A)

1. **GPTSwarm: Language Agents as Optimizable Graphs**
   - **저자/연도**: Zhuge et al. (2024) · `https://arxiv.org/abs/2402.16823`
   - **핵심 요약**: 에이전트를 연산 그래프로 표현해 노드 단위 프롬프트 최적화와 엣지(토폴로지/라우팅) 최적화를 분리 수행.

2. **GraphBit: A Graph-based Agentic Framework for Non-Linear Agent Orchestration**
   - **저자/연도**: Sarker et al. (2026) · `https://arxiv.org/abs/2605.13848`
   - **핵심 요약**: LLM 프롬프트에만 의존하는 라우팅이 환각 전이와 무한 루프를 유발함을 입증. 엔진 제어 DAG + 타입 함수 + 3계층 격리 메모리로 GAIA 67.6%(프레임워크 환각 0%) 달성.

3. **From Static Templates to Dynamic Runtime Graphs: A Survey of Workflow Optimization for LLM Agents**
   - **저자/연도**: Yue et al. (2026) · `https://arxiv.org/abs/2603.22386`
   - **핵심 요약**: 워크플로우를 Agentic Computation Graph(ACG)로 체계화하고, 검증기·트레이스 피드백 기반 정적 vs 동적 런타임 그래프 최적화를 비교.

4. **AgentSPEX: An Agent SPecification and EXecution Language**
   - **저자/연도**: Wang et al. (2026) · `https://arxiv.org/abs/2604.13346`
   - **핵심 요약**: 워크플로우 토폴로지를 코드와 분리한 선언적 DSL을 검증된 하네스(툴 샌드박스·체크포인트·리플레이) 위에서 실행.

5. **VERSE: Verified Self-Evolving Optimizer**
   - **핵심 요약**: 결정적 실행 검증기 없는 자기 진화 루프는 실패하나, 실행 기반 검증기로 게이팅할 때 최고 성능(+72.5% 협업 과제 향상) 달성.

---

## D. Multi-Technique Combinations & Verifier Harnesses (2차 Query B)

1. **SoK: Agentic Retrieval-Augmented Generation (RAG)**
   - **저자/연도**: Mishra et al. (2026)
   - **핵심 요약**: Agentic RAG를 유한 지평 POMDP로 정형화하고 자율 루프의 4대 위험(연쇄 환각 전파, 메모리 오염, 검색 불일치, 연쇄 툴 실행 취약점) 도출.

2. **Retrieval-Augmented Generation (RAG) — From Modular to Agentic Systems**
   - **저자/연도**: Dong et al. (2026), ACM SIGKDD 2026
   - **핵심 요약**: 2020–2026년 약 2,000편 논문 분석을 통해 모듈형 RAG에서 Graph 강화·RL 기반 에이전틱 파이프라인으로의 진화와 선택적 트리거링의 중요성 제시.

3. **EA-GraphRAG & Complexity-Aware RAG Routing**
   - **핵심 요약**: 단순/직접 질의에서는 그래프 순회 노이즈로 GraphRAG가 Vector RAG보다 성능이 떨어짐을 확인. 구문 복잡도 점수에 따라 Vector RAG와 GraphRAG로 동적 라우팅.

4. **Self-RAG / CRAG (Corrective RAG)**
   - **저자/연도**: Asai et al. / Yan et al.
   - **핵심 요약**: 경량 검색 평가기와 반성 토큰을 결합해 컨텍스트 품질을 채점하고, 재분해-재구성 필터링 또는 웹 폴백을 트리거(Context + Loop).

5. **DISC (Denoising Iterative Self-Correction) & MALT**
   - **핵심 요약**: 외부 근거 없는 LLM 자기성찰은 정답을 오히려 훼손할 수 있음을 규명. DISC는 이진 게이트로 해로운 재작성을 차단하고, MALT는 생성자·검증자·개선자를 서로 다른 모델/에이전트로 분리.

6. **Deterministic Orchestration & Capability Fencing**
   - **핵심 요약**: 통제 벤치마크에서 결정적 제어를 갖춘 단일 에이전트(94.4%)가 LLM 자유 오케스트레이션 멀티에이전트(74.4%)를 앞섰으며, 최소 권한 Capability Fencing + 검증 게이트 적용 시 멀티에이전트 성공률이 53.5% → 92.0%로 상승하고 프롬프트 인젝션이 71% → 11%로 급감.

---

## E. Frontier Reasoning Models, Over-Prompting & Visual UI Bias (3차 Query 3)

1. **Pattern over Pixels: Measuring Pattern Completion Bias in Multimodal Code Generation**
   - **저자/연도**: Nguyen et al. (2026) · ACM DOI [`10.1145/3832783.3834443`](https://dl.acm.org/doi/10.1145/3832783.3834443)
   - **핵심 요약**: 반복 UI 패턴이 주어지면 프론티어 멀티모달 LLM이 내부 추론에서는 이상 요소를 인지하고도 최종 코드에서는 패턴 일관성에 맞춰 틀린 UI를 출력하는 편향(글꼴 크기 교란 시 평균 최대 **80.22%**)을 보임 → 지각 기반 스크린샷 검증 루프 필수.

2. **Same Task, Different Work: Prompt-Induced Waste in Coding Agents**
   - **저자/연도**: Weinberger & Hozez (2026) · `https://arxiv.org/abs/2608.01347`
   - **핵심 요약**: 4,644회 코딩 에이전트 실행 분석 결과, "여러 접근법(multiple approaches)" 지시는 성공률 향상 없이 토큰을 **2.4×–7.4×** 부풀리고, "최대 확신(maximum certainty)" 지시는 **18×** 비용의 중복 검증 루프를 유발함.

3. **Thinking Past the Answer: Evaluating Harmful Overthinking in Large Reasoning Models**
   - **저자/연도**: Caldarella et al. (2026) · `https://arxiv.org/abs/2606.02835`
   - **핵심 요약**: 모델이 조기에 정답에 도달하고도 과잉 사고로 답을 망치는 현상을 규명(최초 정답 프리픽스에서 중단 시 정확도 최대 **+21%**).

4. **Prompting Science Report 2: The Decreasing Value of Chain of Thought in Prompting**
   - **저자/연도**: Meincke et al. (2025) · `https://arxiv.org/abs/2506.07142`
   - **핵심 요약**: 내장 추론(reasoning) 모델에는 명시적 CoT 프롬프트가 정확도 이득 없이 토큰·지연·분산만 증가시킴.

5. **Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse**
   - **저자/연도**: Liu et al. (2024) · `https://arxiv.org/abs/2410.21333`
   - **핵심 요약**: 직관·지각·전체적 일관성이 중요한 과제에서 과잉 단계별 숙고가 오히려 성능을 최대 **36.3%p** 하락시킴.

6. **Don't Overthink it & Do LLMs Overthink Basic Math Reasoning?**
   - **저자/연도**: Hassid et al. (2025, `https://arxiv.org/abs/2505.17813`) · Srivastava et al. (2025/2026, `https://arxiv.org/abs/2507.04023`)
   - **핵심 요약**: 짧은 추론 체인이 가장 긴 체인보다 최대 **34.5%** 더 정확할 수 있으며, 단순 문제에 `high` effort를 남용하면 ~18× 토큰만 소모하고 정확도 이득이 없음 → 난이도별 `low`/`medium`/`high` 티어 라우팅의 직접적 근거.

---

## F. Hierarchical Skill Taxonomy & Scaling Interference (4차 Query 4)

1. **When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail**
   - **저자/연도**: Li (2026) · `https://arxiv.org/abs/2601.04748`
   - **핵심 요약**: 스킬 수가 임계점(~50–60개 혼동 가능 도구)을 넘으면 의미 혼동으로 인한 급격한 상전이(phase collapse) 발생. 계층적 라우팅으로 결정 공간을 분할해야 붕괴를 막을 수 있음.

2. **A Formal Hierarchical Architecture for Agentic Orchestration with Stack-Based Execution and Lazy Discovery**
   - **저자/연도**: Devadiga et al. (2026) · `https://arxiv.org/abs/2607.11138`
   - **핵심 요약**: 루트 트리의 현재 활성 노드 직계 자식만 지연 노출(lazy discovery)해 컨텍스트·메모리 비용을 $O(N)$에서 $O(\text{depth})$로 축소하고 분기 간 오염 차단.

3. **SkillDAG: Self-Evolving Typed Skill Graphs for LLM Skill Selection at Scale**
   - **저자/연도**: Bai et al. (2026) · `https://arxiv.org/abs/2606.03056`
   - **핵심 요약**: 평면 벡터 검색은 스킬 간 선행(`requires`), 상호배타(`conflicts_with`), 특화 관계를 포착하지 못함. 타입 DAG 도입 시 스킬 풀 10× 확장에도 순위 안정성 유지(+12.8점).

4. **HiSkill (`arXiv:2607.25853`), Hi-RAG (`doi:10.1111/exsy.70341`) & Adapt the Interface (`doi:10.5281/zenodo.19228710`)**
   - **핵심 요약**: Hi-RAG는 2단계 계층 검색으로 토큰 최대 **89%** 절감; `Adapt the Interface`는 1.5B 소형 모델도 계층 이웃 내에 배치되면 **89%** 도구 선택 정확도를 달성함을 입증(모델 크기보다 인터페이스 계층 구조가 핵심).



