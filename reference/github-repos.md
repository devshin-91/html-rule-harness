# GitHub Repository References (`reference/github-repos.md`)

본 문서는 HTML 분기형 규칙 시스템 및 Google Harness² 적용 설계에 직접 참고·코드 열람한 GitHub 저장소들을 체계화합니다.

## 1. Google Research — `google-research/harness2`
- **URL**: `https://github.com/google-research/harness2` (논문: `arXiv:2610.14224`)
- **검증한 핵심 파일**: `README.md`, `harness2/core/spec.py`, `harness2/core/tree.py`, `harness2/core/prompts.py`, `harness2/core/library.py`, `harness2/core/recursion.py`, `harness2/core/context.py`, `harness2/substrate/codex.py`, `harness2/substrate/opencode.py`
- **설계에 반영한 핵심 아이디어**:
  1. **8-Component Editable Surface & Always-On Budget**: `CODEX_SURFACE`에서 `AGENTS.md`는 `always_on_max=8_000` 자로 상한 제한되며, 상시 텍스트 대신 온디맨드 스킬(`.agents/skills/<name>/SKILL.md`)과 결정적 스크립트(`scripts/*.py`)를 우선 사용한다.
  2. **Skill Trigger Invariant (`_check_skills`)**: `AGENTS.md`에 스킬 이름이 원문 그대로(verbatim) 트리거 문구로 등록되지 않으면 dead weight로 간주해 검증 실패 처리한다 (`scripts/validate_harness.py`에 동일 반영).
  3. **Task-Level Recursion (Propose–Probe–Compose)**: 수정 제안 → 실측 검증(토큰/경로 정확도) → 최소 형태로 합성.
  4. **Harnessing-Level Recursion (`library/`)**: `INDEX.md` + `EXPERIENCE.md`(`cue`, `lesson`, `evidence`, `confidence`)로 교훈을 축적.

## 2. Open Standard — `agentsmd/agents.md`
- **URL**: `https://github.com/agentsmd/agents.md`
- **검증한 파일**: `AGENTS.md`, `README.md`
- **반영 포인트**: 벤더 중립적 AI 에이전트 표준 진입점(`AGENTS.md`)을 루트에 두고, 프로젝트 실행 커맨드와 핵심 제약만 간결한 표·불릿으로 제공한다.

## 3. Multi-Tool Rule Sync — `intellectronica/ruler`
- **URL**: `https://github.com/intellectronica/ruler`
- **검증한 파일**: `README.md`, `.ruler/AGENTS.md`
- **반영 포인트**: `.ruler/` 단일 원천에서 여러 AI 도구(`AGENTS.md`, `CLAUDE.md`, `.agent/rules/`, Copilot 등)로 배포하는 개념과 디렉터리 계층별 중첩(`--nested`) 규칙 로딩 패턴. 우리 프로젝트에서는 HTML 노드를 단일 원천으로 삼고 `validate_harness.py`가 UI 데이터(`tree-data.js`)를 자동 동기화하도록 차용함.

## 4. Agent Skills Spec — `anthropics/skills`
- **URL**: `https://github.com/anthropics/skills` (표준 명세: `https://agentskills.io/specification`)
- **검증한 파일**: `README.md`, `spec/agent-skills-spec.md`, `skills/skill-creator/SKILL.md`
- **반영 포인트**:
  - 3단계 Progressive Disclosure: (1) Metadata (`name` + `description` 상시 광고) → (2) `SKILL.md` 본문(트리거 시 로드) → (3) `scripts/`, `references/`, `assets/`(필요 시 실행/열람).
  - 스킬 `description`을 트리거 상황 중심으로 명확히 작성해 undertriggering 방지.

## 5. Model Complexity Routing — `lm-sys/RouteLLM`
- **URL**: `https://github.com/lm-sys/RouteLLM` (논문: `arXiv:2406.18665`)
- **검증한 파일**: `README.md`
- **반영 포인트**: 모든 질의를 단일 최상위 모델에 보내지 않고, 비용 임계값(threshold)과 라우터(`mf`, `sw_ranking`, `bert`, `causal_llm`)로 단순 질의는 경량 모델에, 고난도 질의는 상위 모델에 분배하는 아키텍처(README 보고 기준 MT Bench에서 GPT-4 성능 95% 유지하면서 비용 최대 85% 절감).

## 6. 기타 탐색 저장소 (Web Search 확인)
- **`github/awesome-copilot`**: `.instructions.md`, `.agent.md` 및 3단계 Progressive Disclosure 패턴.
- **`vllm-project/semantic-router`**: 다중 신호(문맥 길이, 툴 루프 형태, 추론 난이도) 기반 티어(`tier:complex` 등) 라우팅.
- **`UIUC LLMRouter`**: `ThresholdRouter` 등 16개 이상 라우팅 전략 및 난이도 기반 비용-품질 트레이드오프 프레임워크.
