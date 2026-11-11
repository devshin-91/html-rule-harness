# Reference Index (`reference.md`)

작업에 실제로 도움과 근거를 제공한 GitHub 저장소, 웹 문서, Liner Scholar 학술 논문을 `reference/` 아래에 체계화했습니다.

## 1. GitHub Repositories → [`reference/github-repos.md`](./reference/github-repos.md)
- `google-research/harness2` (`arXiv:2610.14224`): Google Harness² 8-component surface, `Propose–Probe–Compose`, Experience Library, `AGENTS.md` 8,000자 상한 및 Skill 트리거 불변식
- `agentsmd/agents.md`: 벤더 중립 `AGENTS.md` 표준
- `intellectronica/ruler`: 단일 원천 → 다중 에이전트 규칙 배포 및 중첩 규칙 패턴
- `anthropics/skills` (`agentskills.io`): 3단계 Progressive Disclosure `SKILL.md` 명세
- `lm-sys/RouteLLM` (`arXiv:2406.18665`): 비용-품질 임계값 기반 모델 라우팅
- 기타 웹 확인 저장소: `github/awesome-copilot`, `vllm-project/semantic-router`, `UIUC LLMRouter`

## 2. Web Docs & Specifications → [`reference/web-and-specs.md`](./reference/web-and-specs.md)
- Antigravity Customization Docs (`rules.md`, `skills.md`): `24 KB` 파일 한도, `20,000` 토큰 규칙 예산, Progressive Disclosure
- ETH Zurich (`arXiv:2602.11988`): 비대한 컨텍스트 파일이 토큰 비용 +20% 및 성능 저하를 유발함을 실증
- XML/HTML 태그 구획화 모범 사례 & 계층 라우팅 arXiv 문헌 (`HierRouter`, `ACRouter`, `HAPO`)

## 3. Liner Scholar Academic Papers → [`reference/liner-scholar-papers.md`](./reference/liner-scholar-papers.md)
- Liner Scholar 탐색 기록 (1차~6차 학술 탐색 세션)
- **Context & Routing**: `arXiv:2605.29270`, `arXiv:2610.02472`, `arXiv:2607.17598` (깊이 제한), `arXiv:2510.04618` (ACE), `arXiv:2410.10347` (Cascade Routing), `arXiv:2510.27042` (e1 Effort), `arXiv:2509.25426` (RADAR)
- **Orchestration, Graph & Combo Patterns**: `GPTSwarm` (`arXiv:2402.16823`), `GraphBit` (`arXiv:2605.13848`), `arXiv:2603.22386`, `AgentSPEX` (`arXiv:2604.13346`), `VERSE`, `SoK: Agentic RAG`, `EA-GraphRAG`, `Self-RAG/CRAG`, `DISC/MALT`, `Capability Fencing`
- **Frontier Reasoning & Visual Bias**: `Pattern over Pixels` (`10.1145/3832783.3834443`), `arXiv:2608.01347` (Prompt-Induced Waste), `arXiv:2606.02835` (Harmful Overthinking), `arXiv:2506.07142`, `arXiv:2410.21333`, `arXiv:2505.17813`, `arXiv:2507.04023`
- **Hierarchical Skill Taxonomy**: `arXiv:2601.04748` (Phase Collapse), `arXiv:2607.11138` (Lazy Discovery), `SkillDAG` (`arXiv:2606.03056`), `HiSkill` (`arXiv:2607.25853`), `Hi-RAG`, `Adapt the Interface` (`zenodo.19228710`)

## 4. AI Engineering Patterns & Multi-Technique Combos → [`reference/ai-engineering-patterns.md`](./reference/ai-engineering-patterns.md)
- `langchain-ai/langgraph`, `google/adk-python` (ADK 2.0), `stanfordnlp/dspy`, `microsoft/graphrag`, `mem0ai/mem0`, `pydantic/pydantic-ai` (`Pydantic AI Harness`, `Pydantic Graph`, `Pydantic Evals`)
- Anthropic *Building Effective Agents* & *Effective Context Engineering*; 5대 기법(Prompt/Context/Harness/Loop/Graph) 및 조합 매트릭스

## 5. Frontier Exceptional Craft & Community Techniques → [`reference/frontier-community-craft.md`](./reference/frontier-community-craft.md)
- GitHub 스킬·시스템 프롬프트: `anthropics/skills` (`frontend-design`, `canvas-design`), Antigravity `generative_ui`, `x1xhlol/system-prompts-and-models-of-ai-tools` (`v0`, `Lovable`, `Cursor`, `Manus`)
- SNS·커뮤니티·블로그·연계 사이트: Anti-Slop / C.L.A.S.S. / 3 Design Dials, Playwright `Slop Inventory` 스크린샷 루프, `21st.dev` / `v0.dev` / `shadcn/ui` / `Magic UI`, 벤더 공식 Frontier 가이드(과잉 프롬프팅 회피 & `reasoning_effort`/`thinkingLevel`)

## 6. Skill Hierarchy & Supply-Chain Security → [`reference/skills-hierarchy-and-security.md`](./reference/skills-hierarchy-and-security.md)
- 바이브 코딩 스킬 모음 한계: `obra/superpowers`, `everything-claude-code`, `awesome-claude-skills`, `BMAD`, `skills.sh`
- 평면 스킬 실패 문헌: `arXiv:2605.24050` (Skill Shadowing), `HiSkill` (`arXiv:2607.25853`), `HERAKLES` (`arXiv:2508.14751`), `SKILLCLASH`, `SkillDAG`, `Toollery` 등
- **3차/4차 요약**: *ToxicSkills* (36%+ 결함, 13%–26% 악성), *Skill-Inject*, NVIDIA *SkillSpector* 패턴 → [`scripts/scan_skills_security.py`](./scripts/scan_skills_security.py) 구현

## 7. UI/UX Research, Argument Calibration & Commercially-Free Stock Credits → [`reference/ui-ux-and-stock-credits.md`](./reference/ui-ux-and-stock-credits.md)
- **상업적 무료 오픈소스 스톡 & 크레딧**: **Lucide Icons** (`v0.460.0`, ISC), **Pretendard Variable** (SIL OFL 1.1), **IBM Plex Sans KR** (SIL OFL 1.1), **JetBrains Mono** (SIL OFL 1.1) + [`rules/assets/licenses/`](./rules/assets/licenses/) 라이선스 정본 번들
- **HCI UI/UX 근거**: NN/g Progressive Disclosure, Laws of UX, Forsey et al. (2024), Springer & Whittaker (2019), Pirolli & Card Information Foraging
- **논증 난이도·Effort 실증 논문 (5차 세션)**: *THOUGHTTERMINATOR* (`arXiv:2504.13367`), *When More is Less* (`arXiv:2502.07266`), *Thinking Past the Answer* (`arXiv:2606.02835`), *Don't Think Twice!* (`arXiv:2508.15050`), *LLM Sycophancy Under User Rebuttal* (`arXiv:2509.16533`), *e1 Adaptive Effort* (`arXiv:2510.27042`)

## 8. Model Switching vs. Effort Scaling Across Tasks → [`reference/model-switching-and-effort.md`](./reference/model-switching-and-effort.md)
- **모델 벤더 공식 제어 & 전환 기준**: OpenAI `reasoning.effort` / Anthropic Adaptive Thinking (`Sonnet high 초과 → Opus medium`) / Google Gemini `thinking_level` (`Flash 1M 컨텍스트 vs Pro 상충 추론`)
- **Liner Scholar 6차 세션  실증 임계치**: *Scaling Test-Time Compute* (`arXiv:2408.03314`), *Reasoning Floor* (`arXiv:2504.14047`, `arXiv:2510.03605`), *Modal Ceiling* (`arXiv:2606.28661`), *Thinking Longer SWE* (`arXiv:2503.20522`), *SWE-Replay* (`arXiv:2601.22129`), *Interaction Scaling* (`arXiv:2607.11598`), *RAG Re-ranker Compute* (`arXiv:2603.14635`, `+7.5 NDCG@10`), *T2MO* (`arXiv:2608.08528`)

## 7. 실증 A/B 벤치마크 및 체크포인트 캐시 레퍼런스 (Phase 7)
- [`benchmark/AB_BENCHMARK_REPORT.md`](./benchmark/AB_BENCHMARK_REPORT.md): 그룹 A(Google Harness² 단독 + `Gemini 4 Argon (Medium)` 고정) 대 그룹 B(Google Harness² + HTML 분기형 규칙 + 작업별 `Argon Low/Medium/High` 매핑) 실측 시간·토큰·품질 비교 리포트.
- [`benchmark/ab_harness.py`](./benchmark/ab_harness.py) & [`benchmark/cache/ab_checkpoint.json`](./benchmark/cache/ab_checkpoint.json): 세부 작업별 트랜스크립트 토큰(`input_tokens`, `cache_read_tokens`, `output_tokens`), 소요 시간, 자동 검증 루브릭 점수 및 쿼터 스냅샷을 기록하는 중단 복구용 체크포인트 캐시.
