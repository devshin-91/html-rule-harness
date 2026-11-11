# Web Docs & System Specifications (`reference/web-and-specs.md`)

본 문서는 웹 문서·플랫폼 공식 가이드·arXiv 문헌에서 확인하고 설계에 반영한 핵심 근거를 정리합니다.

## 1. Antigravity Customization System (로컬 내장 공식 가이드)
- **출처**: `agy-customizations/SKILL.md`, `docs/rules.md`, `docs/skills.md`
- **핵심 제약**:
  - 규칙 탐색: 프로젝트 루트까지 상향 탐색하며 `GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md` 발견 및 경로 기반 자동 중복 제거.
  - 파일당 한도: `24,000` bytes (`@[label](path)` 확장 후 기준).
  - 총 규칙 예산: `20,000` tokens (`defaultRulesBudget`), 초과 시 인라인 대신 파일 경로 포인터로 강등.
  - Progressive Disclosure: `SKILL.md`는 `name`·`description`만 초기 주입하고 선택 시 본문 로드.

## 2. Context File Bloat 실증 연구 (ETH Zurich & LogicStar.ai)
- **논문**: *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* (`arXiv:2602.11988`)
- **핵심 결과**:
  - LLM이 자동 생성한 컨텍스트 파일은 작업 성공률을 오히려 약 2~3% 소폭 하락시키고 추론·토큰 비용을 20% 이상 증가시킴.
  - 인간이 작성한 파일도 약 4%의 소폭 향상 대비 19~20% 토큰 오버헤드를 유발함.
- **설계 시사점**: 루트 `AGENTS.md`는 극도로 슬림하게 유지하고, 세부 규칙은 필요 분기에서만 온디맨드로 읽는 **HTML 분기형 Progressive Disclosure**가 필수적임.

## 3. XML/HTML 태그 기반 프롬프트 구획화 & 분기 패턴
- **근거**: Anthropic/OpenAI 프롬프트 엔지니어링 가이드 및 `agentskills.io/specification`
- **핵심 원칙**:
  - `<active_rule_packet>`, `<rules>`, `data-*` 속성 같은 구조화 경계 태그는 모델의 주의 집중(Attention Anchoring)과 결정적 파싱에 유리함.
  - `<!-- AI-RULE-START --> ... <!-- AI-RULE-END -->` 구획과 외부 CSS/JS 분리를 통해 사람용 미려한 HTML UI와 AI용 최소 컨텍스트를 동시에 달성 가능.

## 4. 난이도 기반 계층적 모델 라우팅 문헌 (Web/arXiv 검색)
- **HierRouter** (`arXiv:2511.09873`): 다중 홉 추론에서 프롬프트 난이도·상태·누적 비용을 평가해 경량/전문화 모델 계층을 동적으로 선택.
- **ACRouter / Agent-as-a-Router** (`arXiv:2606.22902`): 정적 분류기의 정보 결핍을 보완하기 위해 Context–Action–Feedback 루프와 메모리 기반으로 모델 성능-비용 후회를 최적화.
- **HAPO** (`arXiv:2601.02683`): 프롬프트 전체를 뭉뚱그려 고치지 않고 의미 단위(semantic unit)로 귀인·최적화해 기존 성공 규칙의 회귀(prompt drift)를 방지.
