# Project Progress (`progress.md`)

- **프로젝트 루트**: `.`
- **적용 하네스**: Google Harness² (`google-research/harness2`, `arXiv:2610.14224`)

## 완료된 단계

### Phase 1: HTML 분기형 규칙 시스템 & Google Harness² 기본 골격
1. **Harness² 프로젝트 골격**: [`AGENTS.md`](AGENTS.md) (`3,127 chars / 8,000 cap`), [`rules.md`](rules.md), `.agents/skills/` (6개 온디맨드 스킬), [`library/INDEX.md`](library/INDEX.md) & [`library/EXPERIENCE.md`](library/EXPERIENCE.md) (Iteration 01→04 기록).
2. **HTML 분기 트리 (Depth 0~3)**: [`rules/router.html`](rules/router.html) + `rules/branches/{reasoning,coding,research,meta}/*.html`, [`rules/model-catalog.json`](rules/model-catalog.json), [`rules/index.html`](rules/index.html) 인터랙티브 대시보드.
3. **결정적 탐색·검증 도구**: [`scripts/resolve_rule.py`](scripts/resolve_rule.py), [`scripts/validate_harness.py`](scripts/validate_harness.py), [`tests/test_rules_harness.py`](tests/test_rules_harness.py).
4. **1차 레퍼런스 체계화**: [`reference.md`](reference.md), [`reference/github-repos.md`](reference/github-repos.md), [`reference/web-and-specs.md`](reference/web-and-specs.md), [`reference/liner-scholar-papers.md`](reference/liner-scholar-papers.md).

### Phase 2: AI 유즈케이스 (Prompt / Context / Harness / Loop / Graph & 조합) 통합
5. **AI 유즈케이스 5대 기법 & 복합 조합 분기 확장 (`rules/branches/ai-systems/`)**:
   - `ai-systems.root` (`index.html`) + 6개 Depth-2 분기: `prompt-opt.html`, `context-rag.html`, `harness-guard.html`, `agent-loop.html`, `graph-orch.html`, `combo-recipes.html`.
   - 모든 주요 리프·유즈케이스 노드에 `data-pillars` 속성 및 동적 다중 기법 신호(`PILLAR_SIGNALS`) 반영.
   - 신규 스킬 [`.agents/skills/ai-architecture-stack/SKILL.md`](.agents/skills/ai-architecture-stack/SKILL.md) 추가 및 `AGENTS.md` 트리거 등록.
   - UI 확장: [`rules/assets/rule-ui.js`](rules/assets/rule-ui.js) & [`rules/assets/rule-ui.css`](rules/assets/rule-ui.css)에 5-Pillar 시각화 칩 및 AI 유즈케이스 프리셋 추가.
6. **AI 유즈케이스 레퍼런스 (`reference/ai-engineering-patterns.md`, `reference/liner-scholar-papers.md`)**:
   - GitHub 저장소(`langgraph`, `adk-python`, `dspy`, `graphrag`, `mem0`, `pydantic-ai`) 및 Anthropic 가이드 정리.
   - Liner Scholar 2차 탐색 완료(크레딧 가드 기준 `> 100` 준수): `GPTSwarm`, `GraphBit`, `AgentSPEX`, `VERSE`, `SoK: Agentic RAG`, `EA-GraphRAG`, `CRAG/Self-RAG`, `DISC/MALT`, `Capability Fencing` 논문의 실증 규칙을 `context-rag.html`, `agent-loop.html`, `graph-orch.html`, `combo-recipes.html`에 직접 반영 완료.
7. **트레이드오프 & 검증**:
   - [`tradeoff.md`](tradeoff.md) 갱신 완료.
   - `validate_harness.py`: `24` HTML 노드, `7` 스킬, `0` 에러 (`tree-data.js` 동기화 완료).
   - `unittest`: `7/7` 통과, `node --check` 통과.

### Phase 3: 최상위(Frontier) 모델 탁월한(Exceptional) 크래프트 · 커뮤니티/SNS/연계 사이트 기법 통합
8. **최상위 모델 전용 분기 & 스킬 (`frontier-craft`)**:
   - [`rules/branches/ai-systems/frontier-craft.html`](rules/branches/ai-systems/frontier-craft.html) (`tier: high`, `effort: high`, `pillars: prompt,harness,loop`) 및 [`.agents/skills/frontier-craft/SKILL.md`](.agents/skills/frontier-craft/SKILL.md) 추가, `AGENTS.md` 트리거 등록.
   - [`rules/branches/meta/model-router-policy.html`](rules/branches/meta/model-router-policy.html)에 최상위 모델 과잉 프롬프팅(Over-Prompting) 금지 규율 반영, [`rules/assets/rule-ui.js`](rules/assets/rule-ui.js)에 `[Frontier]` 시뮬레이터 프리셋 추가.
9. **GitHub · 커뮤니티/SNS · 연계 사이트 · Liner Scholar 3차 체계화**:
   - [`reference/frontier-community-craft.md`](reference/frontier-community-craft.md): `anthropics/skills` (`frontend-design`, `canvas-design`), `generative_ui`, `x1xhlol/system-prompts-and-models-of-ai-tools`, 커뮤니티 Anti-Slop / Design Dials / Playwright `Slop Inventory` 루프, `21st.dev`·`v0.dev`·`shadcn/ui`·`Magic UI`, 벤더 공식 Frontier 가이드 정리.
   - [`reference/liner-scholar-papers.md`](reference/liner-scholar-papers.md) 섹션 E 추가 (3차 탐색, 크레딧 가드 기준 `> 100` 준수): `Pattern over Pixels`, `arXiv:2608.01347`, `arXiv:2606.02835`, `arXiv:2506.07142`, `arXiv:2410.21333`, `arXiv:2505.17813`, `arXiv:2507.04023`.

### Phase 4: 스킬 위계·분기 구조화 & 악성 스킬 보안 게이트
10. **4계층 스킬 위계 & 선행·충돌 해소**:
    - [`rules/skill-hierarchy.json`](rules/skill-hierarchy.json) 및 `resolve_rule.py`(`order_skill_pipeline`), `rule-ui.js`에 4계층(`T0:gate → T1:plan → T2:execute → T3:verify`) 파이프라인 정렬과 `requires`/`conflicts_with` 해결 반영.
    - [`rules/branches/meta/skill-hierarchy.html`](rules/branches/meta/skill-hierarchy.html) 추가 및 `meta/index.html` 연결.
11. **악성 스킬 탐지·차단 게이트**:
    - [`scripts/scan_skills_security.py`](scripts/scan_skills_security.py) (간접 인젝션, `curl|bash`, `.ssh/.aws`, 은닉 유출, `os.environ`+네트워크 송신 등 7종 탐지) 구현 및 `validate_harness.py` 자동 통합.
    - [`.agents/skills/skill-security-audit/SKILL.md`](.agents/skills/skill-security-audit/SKILL.md) + [`rules/branches/meta/skill-security.html`](rules/branches/meta/skill-security.html) 추가 및 `AGENTS.md` 트리거 등록.
12. **스킬 위계·보안 레퍼런스 & 최종 검증**:
    - [`reference/skills-hierarchy-and-security.md`](reference/skills-hierarchy-and-security.md) 및 [`reference/liner-scholar-papers.md`](reference/liner-scholar-papers.md) 섹션 F(4차 세션) 정리.
    - `validate_harness.py` (`26` HTML 노드, `8` 스킬, `0` 에러), `scan_skills_security.py` (`passed: true`), `tests/test_rules_harness.py` (`9/9` 통과).

### Phase 5: 실증 논증 계층화·Effort 우선 보정 · Anti-Slop UI/UX 개편 & 오픈소스 스톡 크레딧
13. **논증 난이도·Effort 실증 보정 & 라우팅 정확도 수정**:
    - [`rules/branches/reasoning/structured-argument.html`](rules/branches/reasoning/structured-argument.html) (`mid / medium`) 신설 — 찬반·반론 재반박·숨은 가정 감사 논증을 `low`(`simple-argument`) 및 `high`(`deep-synthesis`)와 실증 분리(`arXiv:2504.13367`, `arXiv:2508.15050`, `arXiv:2509.16533`).
    - [`scripts/resolve_rule.py`](scripts/resolve_rule.py) 및 [`rules/assets/rule-ui.js`](rules/assets/rule-ui.js)에 **1단계 동일 티어 내 Effort 우선 보정(`low→medium`, `mid→high`)**, 짧은 영문 키워드 단어경계 검사, 한국어 용언·조사 어간 매칭 반영.
    - `"exceptional"` 한국어 오역(`"예외적"`)을 전 파일에서 `"탁월한 / 뛰어난 / 특별한"` 맥락으로 교정 완료.
14. **현대적 Editorial UI/UX 개편 & 상업적 무료 스톡 크레딧**:
    - 기존 AI Slop 다크-인디고/바이올렛 카드 및 2컬럼 오버플로우/XML 잘림·무음 수동오버라이드 혼동 결함 전면 해소 (`min-width: 0`, `pre-wrap`, 접이식 트리, 검색 `/`, 명시적 `수동 분기 직접 탐색 중` 배너).
    - 상업적 무료 오픈소스 스톡 적용 및 라이선스 번들: **Lucide Icons v0.460.0** (ISC), **Pretendard Variable v1.3.9** (SIL OFL 1.1), **IBM Plex Sans KR** (SIL OFL 1.1), **JetBrains Mono** (SIL OFL 1.1) — [`rules/assets/licenses/`](rules/assets/licenses/), Explorer 푸터 및 [`reference/ui-ux-and-stock-credits.md`](reference/ui-ux-and-stock-credits.md)에 전체 크레딧 명시.

### Phase 6: 작업별 Effort 상향 vs 모델 변경(승격·특화 전환) 실증 체계 통합
15. **벤더 파라미터 & 4대 적응 정책 통합([`rules/model-catalog.json`](rules/model-catalog.json), [`reference/model-switching-and-effort.md`](reference/model-switching-and-effort.md))**:
    - OpenAI `reasoning.effort` · Anthropic `output_config.effort` (`Sonnet high 초과 → Opus medium`) · Google `thinking_level` (`Flash 1M 컨텍스트 vs Pro 상충 추론`) 및 Liner Scholar 6차 세션 실증 임계치 반영.
    - [`scripts/resolve_rule.py`](scripts/resolve_rule.py), [`scripts/validate_harness.py`](scripts/validate_harness.py), [`rules/assets/rule-ui.js`](rules/assets/rule-ui.js), 주요 HTML 노드에 4대 정책(`effort-first-with-verifier`, `capacity-switch-sensitive`, `grounding-over-thinking`, `overthinking-guard-low`)과 `--no-verifier`/UI 검증기 토글에 따른 **`keep_optimal` / `raise_effort` / `switch_model_up` / `ground_before_think`** 결정 로직 반영.
    - 상단 Hero 카드, `AGENTS.md`, `router.html`, `model-router-policy.html`, `<model_candidates role="reference_examples">` XML 패킷에 **참고 모델명 예시 vs 실행 환경 매핑** 및 **일반 규칙 기준선(작업·환경별 편차 존재)** 고지 추가, 우측 시뮬레이터 Sticky Follow-Scroll(`position: sticky`, `overflow-x: clip`) 적용 완료.

## Phase 7: Gemini 4 Argon 실증 A/B 효용성 벤치마크 및 체크포인트 캐시 (`2026-11-12`)
- **쿼터 버킷 분리 실측 확인**:
  - `gemini-3.8-flash-{low,medium,high}` (5시간 롤링 한도, `10%`, 리셋 `2026-11-11T22:34:36Z`)와 `gemini-4-argon-{low,medium,high}` (7일 주간 한도, `95% -> 93%`, 리셋 `2026-11-18T21:35:25Z`)가 별도 쿼터 풀로 동작함을 확인.
- **A/B 벤치마크 하네스 & 체크포인트 캐시 구축**:
  - `benchmark/ab_harness.py`, `benchmark/cache/ab_checkpoint.json`, `benchmark/AB_BENCHMARK_REPORT.md` 생성.
- **실측 대조 결과 (그룹 A: `Argon Medium` 단일 고정 vs 그룹 B: 규칙 기반 `Argon Low/Medium/High` + 단일 `<active_rule_packet>`)**:
  - 규칙 컨텍스트: `74,816 tok` -> `2,473 tok` (**-96.7% 절감**)
  - 실측 신규 입력 토큰 (`input_tokens`): `129,114` -> `85,309` (**-33.9% 절감**)
  - 실측 캐시 읽기 토큰 (`cache_read_tokens`): `266,691` -> `180,312` (**-32.4% 절감**)
  - 실측 총 소모 토큰 (`total_tokens`): `402,239` -> `276,264` (**-31.3% / -125,975 tok 절감**)
  - 작업 소요 시간: 병렬 최장 `90.0s` -> `89.0s` (단순 논증 `T1`은 `27.0s -> 17.0s`, **-37.0% 단축**)
  - 작업 품질·검증 점수: **`92 / 100점` -> `100 / 100점` (+8.0점 향상)**

## Phase 8: v2.0 MD-Source → HTML-Compiled 리팩토링, Anti-Hallucination 가드레일 & Gemini 4 v3.0 카탈로그 (`2026-11-21`)
- **MD 단일 원천 → 결정적 HTML 컴파일 (`md-html-guide` 원칙 적용)**:
  - 28개 규칙 노드를 Markdown + YAML Frontmatter 단일 원천(`rules/src/router.md` + `rules/src/branches/**/*.md`, 총 `45,916 B`)으로 전환하고, 표준 라이브러리 기반 결정적 컴파일러 [`scripts/build_rules_html.py`](scripts/build_rules_html.py) (`--check` 동기화 검증 포함, **0 LLM 토큰**)로 `rules/router.html`, `rules/branches/**/*.html` (`73,564 B`), `rules/assets/tree-data.js`를 생성.
  - [`scripts/resolve_rule.py`](scripts/resolve_rule.py)를 `rules/src/**/*.md` 우선 로드(+ HTML 자동 폴백, `stats.source_format: "md"|"html"`)로 리팩토링.
- **Anti-Hallucination 가드레일 통합 (`antigravity-gemini-anti-hallucination`)**:
  - 신규 분기 [`rules/src/branches/meta/anti-hallucination.md`](rules/src/branches/meta/anti-hallucination.md) (`meta.anti-hallucination`, `tier: high`, `effort: high`) 및 Tier 3 검증 스킬 [`.agents/skills/anti-hallucination-guard/SKILL.md`](.agents/skills/anti-hallucination-guard/SKILL.md) 추가, [`rules/skill-hierarchy.json`](rules/skill-hierarchy.json) v2.0 (9개 스킬) 및 [`AGENTS.md`](AGENTS.md) (`5,395 / 8,000 chars`) 트리거 등록.
  - 공통 4대 원칙(도구 우선·역환각 금지, 선 원문 발췌+`#L` 인용, 모름의 권한·거짓 전제 교정, 실행 기반 검증), 5대 모델 계보 수칙, Tier 0–2 `ref-fact-checker` 및 `Stop` 훅(`max_continuations=2`) 규율 반영.
- **모델 카탈로그 v3.0 업그레이드 ([`rules/model-catalog.json`](rules/model-catalog.json))**:
  - 현역 검증 모델로 전면 갱신: `gemini-3.5-flash-lite`, `gemini-3.8-flash`, `gemini-decision-1` (`v1beta` Decisions API), `gemini-4-hydrogen`, `gemini-4-neon`, `gemini-4-argon`, `gemini-4-carbon` (구세대 레거시 1.x/2.x 모델 0건).
  - 모델별 `thinking_level` 상하한(`carbon`/`argon`: `low`/`medium`[기본]/`high`, `xhigh`·`minimal` 불가; `hydrogen`: `low`/`medium`/`high`[기본]/`xhigh`, `minimal` 불가), 명시적 캐싱·픽셀 세그멘테이션 미지원 경계, Long Decode(`background=True` + `max_output_tokens > 65536`, `total_input_tokens` 압축 트리거 금지) 명세화.
- **Explorer UI v2.0 Export Loop & 검증**:
  - [`rules/index.html`](rules/index.html), [`rules/assets/rule-ui.js`](rules/assets/rule-ui.js), [`rules/assets/rule-ui.css`](rules/assets/rule-ui.css)에 `MD Source → HTML View` 배지·안내 배너, **`JSON 설정 내보내기`** + **`Markdown 규칙 패킷 내보내기`** + 기존 XML 복사 버튼, **`환각 검증 [Anti-Hallucination]`** 프리셋, Markdown 원본 빌더 템플릿 추가.
  - 검증 결과: `build_rules_html.py --check` (28 MD/HTML 노드, `max_node_ai_bytes: 2,764 B <= 2,800 B`), `validate_harness.py` (`md_html_in_sync: true`, `skills: 9`, `model_catalog_version: 3.0`), `scan_skills_security.py` (`0 findings`), `unittest` (**17/17 OK**), `node --check rules/assets/rule-ui.js` (exit 0).

