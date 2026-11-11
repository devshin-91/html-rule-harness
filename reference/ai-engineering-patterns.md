# AI Engineering Patterns & Multi-Technique Combinations (`reference/ai-engineering-patterns.md`)

Prompt / Context / Harness / Loop / Graph 5대 엔지니어링 기법과 다중 기법 조합 레시피를 위해 직접 코드·README·공식 문서를 확인한 GitHub 저장소 및 엔지니어링 가이드 목록입니다.

## 1. 검증한 GitHub 저장소

1. **`langchain-ai/langgraph`** (`https://github.com/langchain-ai/langgraph`)
   - **열람 파일**: `README.md` (라인 1–82)
   - **핵심**: 상태 기반(stateful) 장기 실행 에이전트용 저수준 오케스트레이션 프레임워크(Pregel/Apache Beam/NetworkX 영감).
   - **특징**: Durable Execution(장애 복구·재개), Human-in-the-Loop(상태 검사/수정), 단기·장기 메모리, LangSmith 추적 및 상위 패키지 **Deep Agents**(계획·서브에이전트·파일시스템 활용).

2. **`google/adk-python`** (`https://github.com/google/adk-python`)
   - **열람 파일**: `README.md` (라인 1–180, Agent Development Kit 2.0)
   - **핵심**: `Agent` + 그래프 기반 실행 엔진 `Workflow`를 코드 우선(code-first)으로 결합.
   - **특징**: Routing, Fan-out/Fan-in 병렬, Loops, Retry, 상태 관리, 동적 노드, HITL(Tool Confirmation), Task API 기반 에이전트 간 위임, `adk eval` 평가 CLI 내장.

3. **`stanfordnlp/dspy`** (`https://github.com/stanfordnlp/dspy`)
   - **열람 파일**: `README.md` (라인 1–90)
   - **핵심**: 수작업 프롬프트 대신 선언적 파이썬 모듈로 LM을 프로그래밍하고 자동 최적화(컴파일).
   - **주요 논문 근거**: `GEPA` (`arXiv:2507.19457`, 반성적 프롬프트 진화), `DSPy` (`arXiv:2310.03714`), `DSPy Assertions` (`arXiv:2312.13382`, 계산적 제약 기반 자가정제).

4. **`microsoft/graphrag`** (`https://github.com/microsoft/graphrag`)
   - **열람 파일**: `README.md` (라인 1–79, 논문 `arXiv:2404.16130`)
   - **핵심**: 비정형 텍스트에서 엔티티·관계·커뮤니티 지식 그래프를 추출해 전역(global) 질문 응답을 수행하는 RAG 파이프라인. 인덱싱 비용이 크므로 소규모 검증 후 적용 권고.

5. **`mem0ai/mem0`** (`https://github.com/mem0ai/mem0`)
   - **열람 파일**: `README.md` (라인 1–110)
   - **핵심**: User/Session/Agent 다중 레벨 메모리 계층. Single-pass ADD-only 추출, 엔티티 링킹, Semantic+BM25+Entity 다중 신호 융합 검색, 시간 추론(Temporal Reasoning) 제공 (LoCoMo `92.5`, LongMemEval `94.4` 보고).

6. **`pydantic/pydantic-ai`** (`https://github.com/pydantic/pydantic-ai`)
   - **열람 파일**: `README.md` (라인 1–110 및 graph/durable/evals 섹션)
   - **핵심**: End-to-End 타입 검증 에이전트 루프 + **`Pydantic AI Harness`**(`Coder`, `Advisor`, `ClearToolResults`, `ToolOutputLimits`, `RepairToolArguments`, `SubAgents`, `Compaction`, `Guardrails`) + **`Pydantic Graph`**(타입 제어 흐름) + **`Pydantic Evals`** + Durable Execution(Temporal/DBOS/Prefect 등).

---

## 2. 엔지니어링 가이드 & 기법 조합 매트릭스 (Web Docs)
- **Anthropic — *Building Effective Agents* & *Effective Context Engineering for AI Agents***
  - **핵심 원칙 (Simplicity First)**: 단일 LLM 호출 / Prompt Chaining → Routing → Parallelization(Sectioning/Voting) → Orchestrator-Workers → Evaluator-Optimizer 순으로 복잡도를 올릴 것.
  - **Context Rot 대응**: Compaction, Tool-Result Clearing, 서브에이전트 컨텍스트 격리.
- **4계층 스택 (Prompt → Context → Loop → Harness) + Graph**:
  - **Prompt + Context**: 타입 스키마 강제 출력 + Hybrid RAG/Mem0 검색.
  - **Context + Loop**: Corrective RAG(검색 적합성 평가 → 쿼리 재작성 루프) + Compaction.
  - **Harness + Loop**: 샌드박스/테스트 게이트 훅 + Propose–Probe–Compose 검증 루프(생성자/평가자 컨텍스트 분리).
  - **Graph + Harness + Context**: 상태 그래프(LangGraph/ADK/Pydantic Graph) + 노드별 컨텍스트 격리 + 모델 티어 라우팅 + HITL 체크포인트.
