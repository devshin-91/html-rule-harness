# Frontier Model & Community Craft References (`reference/frontier-community-craft.md`)

최상위(Frontier) 모델로 비주얼·완성도 측면에서 탁월하고 뛰어난(Exceptional) 결과물을 도출하기 위해 GitHub, 공식 프롬프팅 가이드, SNS(X)·블로그·커뮤니티(Reddit/HN) 공개 기법을 조사해 정리한 문서입니다.

## 1. GitHub 공개 스킬 및 시스템 프롬프트 저장소
1. **`anthropics/skills` — `frontend-design` & `canvas-design`** (직접 파일 열람 완료)
   - `frontend-design/SKILL.md`: 2-Pass 설계(짧은 디자인 플랜 먼저 작성 후 일반적 기본값인지 자기검토), **"Spend your boldness in one place"**, AI 클리셰(warm-cream+terracotta, track-out ALL-CAPS eyebrow, 획일 SaaS 카드) 회피, 스크린샷 기반 자기 비평("a picture is worth 1000 tokens").
   - `canvas-design/SKILL.md`: 1단계 **Visual Philosophy / Aesthetic Manifesto** 먼저 선언 후 2단계 시각 표현 분리, 장인정신 프레이밍과 창의적 여백(creative space) 보장.
2. **Antigravity 내장 `generative_ui` 스킬** (직접 열람 완료)
   - 호스트 테마 시맨틱 변수(`--card`, `--foreground`, `--border`) 강제, 12px 미만 극소 텍스트 금지, `<agent-embed>` vs 독립 아티팩트 분리 기준.
3. **`x1xhlol/system-prompts-and-models-of-ai-tools`** (저장소 구조 및 커뮤니티 분석 확인)
   - `v0`, `Lovable`, `Cursor Prompts`, `Devin AI`, `Google`, `Anthropic`, `Manus` 등 실전 프로덕션 시스템 프롬프트 패턴:
     - **Design System Token Locking** (v0 방식: 팔레트·여백·보더·그림자 체계 명시)
     - **State Completeness** (Lovable 방식: Loading Skeleton, Empty State, Filter/Sort/Focus 등 엣지 상태까지 한 번에 구현 강제)
     - **Anti-Spaghetti Component Hierarchy** (구현 전 컴포넌트 계층 분리)

## 2. 커뮤니티 · SNS(X) · 블로그(Substack / Simon Willison / Reddit / HN) 핵심 기법
1. **Frontier 모델 과잉 프롬프팅(Over-Prompting) 회피**
   - 추론형 최상위 모델(o-series / GPT-5 Pro / Gemini Pro / Opus)에는 레거시 모델용 `"think step by step"` 미세 지시가 오히려 토큰·지연을 부풀리고 추론을 방해함.
   - 대신 **GOLDEN 구조**(Goal / Output / Limits / Data)처럼 **목표·성공 기준·금지 제약**을 선명히 주고 내부 추론 예산(`high`)에 위임함.
2. **Anti-Slop & Taste Dials (커뮤니티 `aiuxplayground.com`, Reddit r/ClaudeAI 등)**
   - **C.L.A.S.S. 프레임워크**: Category · Layout · Aesthetics · Scheme(OKLCH/HEX 토큰) · Specificity.
   - **3개 디자인 다이얼(Design Dials)**: Variance(대칭↔비대칭), Motion Intensity(정적↔시네마틱), Visual Density(여백↔고밀도)를 코드 작성 전 수치·방향으로 고정.
   - **금지 목록(Negative Locks)**: 보라-인디고 기본 그라디언트, 기본 Inter/Roboto 남용, 획일 3열 카드, 미요청 `01/02/03` 배지, 상투적 AI 카피 금지.
3. **Playwright 스크린샷 루프 함정 극복 (`Slop Inventory` + `toHaveScreenshot`)**
   - 단순히 스크린샷을 주며 *"더 예쁘게 고쳐라"*고 반복하면 레이아웃 회귀(무한 루프)가 발생.
   - **해법**: 코드 수정 전 **(a) Slop Inventory(결함 목록) → (b) 유지할 3~5개 강점 → (c) 단 하나의 Signature Move 수정 계획**을 텍스트로 먼저 확정하고, `document.fonts.ready`·애니메이션 고정 후 다중 뷰포트(`375px/768px/1440px`) 검증 또는 **생성 모델(Opus/Gemini Pro)과 리뷰/린터 모델(GPT/Codex) 분리** 적용.

## 3. 프로젝트 연계 공개 사이트 & 공식 프런티어 가이드 (Web Search 확인)
1. **프로젝트 연계 UI·프롬프트 쇼케이스 생태계**:
   - **`v0.dev`** (Vercel): 자연어 프롬프트 → 접근성 준수 React + Tailwind + `shadcn/ui` 프리뷰/반복 생성.
   - **`21st.dev`** (구 Magic MCP): `shadcn/ui` 호환 컴포넌트·블록·애니메이션 오픈 레지스트리 + Cursor/Claude Code용 MCP 연동.
   - **`shadcn/ui` & `Magic UI`**: AI 프론트엔드 생성기가 일관된 품질을 내기 위해 가장 많이 고정하는 시맨틱 컴포넌트·모션(Bento Grid, Framer Motion) 기반.
2. **모델 벤더 공식 Frontier/Reasoning 프롬프팅 가이드**:
   - **OpenAI (GPT-5 시리즈)**: 텍스트 꼼수 대신 `reasoning_effort`, `verbosity`, agentic eagerness 조절 및 Responses API(`previous_response_id`) 활용.
   - **Google Gemini (Thinking / Experimental)**: **Persona–Task–Context–Format** 명시, 대규모 멀티모달/문서 그라운딩에 기반한 분석 위임.
   - **Anthropic Claude (Opus / 고성능 세대)**: 축약 없는 명확한 사전 명세서(up-front spec), 문자 그대로의(literal) 준수 특성 이해 및 Effort 레벨(`low`/`medium`/`high`) 조절.
