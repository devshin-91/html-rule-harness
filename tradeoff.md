# Architecture Trade-offs & Session Handoff Notes (`tradeoff.md`)

본 문서는 HTML 분기형 규칙 시스템의 핵심 설계 트레이드오프와, 세션 컨텍스트 80% 초과 시 새 대화 인계를 위한 판단 근거를 기록합니다.

## 1. HTML 단일 파일 vs 다중 모듈 HTML 트리 + JS 데이터 번들
- **선택**: 다중 모듈 HTML 노드(`rules/router.html`, `rules/branches/**/*.html`) + 외부 `rule-ui.css` / `rule-ui.js` + 자동 생성 `tree-data.js` 기반 `rules/index.html` 대시보드.
- **대안 (기각)**: 모든 규칙·스타일·스크립트를 단일 `rules.html`에 인라인 통합.
- **이유**: 단일 HTML 파일에 CSS/JS/전체 분기를 합치면 AI가 파일을 읽는 순간 수만 토큰이 주입되어 "규칙 반영 컨텍스트 최소화" 목표에 정면 배치됨. 반면 `fetch()` 기반 다중 HTML 로딩은 로컬 `file://` 브라우저에서 CORS 차단이 발생함. 따라서 각 분기 HTML은 초경량 시맨틱 블록(`AI-RULE-START..END`)만 담고, `validate_harness.py`가 `tree-data.js`를 생성해 `file://` 대시보드(`index.html`)까지 무결하게 동작하도록 절충함.

## 2. 규칙 내부 배지 마크업 vs 외부 JS 하이드레이션
- **선택**: `data-depth`, `data-tier`, `data-effort`, `data-skills` 속성만 HTML 노드에 두고 시각적 배지/아이브로우는 `rule-ui.js`가 동적 렌더링.
- **이유**: 한국어 UTF-8 문자는 3바이트이므로 HTML 노드에 시각 배지 텍스트를 중복 배치하면 AI 블록이 2,800B를 쉽게 초과함(Iteration 01 Probe에서 실측 확인). 단일 원천(`data-*`) + JS 하이드레이션으로 AI 블록 크기를 ~35% 절감하면서 인간 UI 품질을 그대로 유지함.

## 3. 모델명 하드코딩 vs 티어(`low`/`mid`/`high`) + 카탈로그(`model-catalog.json`) 탐색
- **선택**: 규칙 분기에는 추상 티어(`low`, `mid`, `high`)와 `effort`, `skills`를 명시하고, 구체적 모델 후보는 `rules/model-catalog.json`과 동적 에스컬레이션 신호(`files`, `attempts`, `concurrency`, `security`)로 탐색·매핑.
- **이유**: 특정 모델 버전(예: 특정 날짜/스냅샷 ID)을 규칙 파일마다 하드코딩하면 모델 세대 교체 시 전체 HTML 트리를 수정해야 함. 추상 티어 + 단일 JSON 카탈로그 분리로 유지보수성과 멀티 프로바이더(Gemini, Claude, OpenAI) 호환성을 확보함.

## 4. 단일 AI 기법 vs 다중 기법 조합(`Prompt / Context / Harness / Loop / Graph`)
- **선택**: 5대 기법을 독립 Depth-2 분기로 분리하되, 복합 시너지를 위한 `ai-systems.combo-recipes`와 동적 `data-pillars` 시그널 추출을 결합.
- **대안 (기각)**: 모든 작업에 무조건 Graph+Loop+RAG 풀스택을 적용.
- **이유**: Anthropic *Building Effective Agents* 원칙대로 단순 호출/Prompt Chaining으로 해결되는 작업에 Graph·자율 루프를 얹으면 지연·토큰·실패 표면이 급증함. 작업 성격에 맞는 최소 기법(또는 필수 조합만)을 선택하도록 분기를 분리함.

## 5. 평면 스킬 모음 vs 4계층 스킬 위계 + 정적 보안 게이트
- **선택**: HTML 분기별 국소 노출($O(\text{depth})$) + [`rules/skill-hierarchy.json`](rules/skill-hierarchy.json)(4계층 `Gate → Plan → Execute → Verify`, `requires`/`conflicts_with`) + [`scripts/scan_skills_security.py`](scripts/scan_skills_security.py) 정적 보안 게이트.
- **대안 (기각)**: 수십~수백 개 `SKILL.md`를 평면 디렉터리로 일괄 등록하고 LLM이 스스로 고르게 방치.
- **이유**: 평면 목록은 Skill Shadowing·블랙홀 스킬 편향·SKILLCLASH(충돌 시 한쪽 덮어쓰기)를 일으키며, 공개 스킬의 36%+ 결함 / 13%–26% 악성 위험에 무방비함. 위계 DAG와 보안 게이트를 `validate_harness.py`에 강제 결합해 해결함.

## 6. 논증 단일 티어 배정 vs 3단계 분화 & 1단계 Effort 우선 보정
- **선택**: 논증 분기를 `simple-argument`(`low`), `structured-argument`(`mid`), `deep-synthesis`(`high`) 3단계로 분리하고, 티어 상향 전 동일 티어 내 Effort 보정(`low→medium`: 28–41점, `mid→high`: 60–74점)을 우선 적용.
- **대안 (기각)**: 모든 논증을 `low` 모델로 처리하거나, 작은 난이도 상승마다 즉시 상위 티어 모델로 점프.
- **이유**: 단순 요약은 과잉 추론 시 역전(`arXiv:2504.13367`, `arXiv:2606.02835`)을 겪으나, 찬반·반론·가정 감사에서는 하위 모델이 아첨(`arXiv:2509.16533`) 및 확신 왜곡(`arXiv:2508.15050`)을 보임. 1단계 Effort 조정 후 필요 시 티어 승격하는 Cascade 구조가 품질과 비용을 동시에 최적화함.

## 7. 정적 AI Slop UI vs 상업적 무료 스톡 기반 Editorial Workbench
- **선택**: Warm Stone Paper(`#F6F5F0`) / Forest Teal(`#0F766E`) 팔레트 + **Lucide Icons**(ISC) + **Pretendard Variable / IBM Plex Sans KR / JetBrains Mono**(SIL OFL 1.1) 및 `rules/assets/licenses/` 정본 라이선스 번들.
- **이유**: 외부 CDN 서체가 차단된 로컬 `file://` 환경에서도 오프라인 번들된 Lucide SVG와 시스템 폴백 스택이 깨지지 않으며, 모든 CSS Grid 아이템에 `min-width: 0`과 `pre-wrap`을 적용해 `375px`~`1280px` 전 뷰포트에서 가로 잘림을 제거함.

## 8. 검증기 유무·역량 하한 기반 Effort 상향 vs 모델 변경 분리
- **선택**: 4대 정책(`effort-first-with-verifier`, `capacity-switch-sensitive`, `grounding-over-thinking`, `overthinking-guard-low`) + `--no-verifier` 신호로 `raise_effort`와 `switch_model_up`, `ground_before_think`를 명시 분리.
- **이유**: 테스트·컴파일러 검증기가 있으면 동일 모델 내 Effort 증가가 14배 큰 모델을 추월할 수 있으나(`Ma 2025`, `Snell 2024`), 검증기가 없으면 모달 천장(`arXiv:2606.28661`)에 갇히며 RAG·사실 조회는 내부 사고가 아닌 검색·리랭킹(`+7.5 NDCG@10`, `arXiv:2603.14635`)이 결정적이므로 획일적 점수 상향을 기각함.

## 9. 세션 인계 체크포인트
- 현재 세션이 길어질 경우(80% 초과 시) 새 대화 세션은 [`AGENTS.md`](AGENTS.md), [`rules.md`](rules.md), [`reference.md`](reference.md), [`progress.md`](progress.md), [`tradeoff.md`](tradeoff.md)를 먼저 로드해 기존 하네스와 전체 설계 컨텍스트를 그대로 승계합니다.
