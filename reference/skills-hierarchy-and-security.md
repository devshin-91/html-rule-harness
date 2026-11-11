# Skill Hierarchy & Supply-Chain Security (`reference/skills-hierarchy-and-security.md`)

바이브 코딩(Vibe Coding)용 GitHub 스킬 모음들의 한계(평면적 나열로 인한 위계·분기 부재)와 악성/위험 스킬 공급망 위협을 조사해 정리한 문서입니다.

## 1. 조사한 유행 스킬 저장소 & 한계
1. **`obra/superpowers`** (직접 클론 및 `README.md`, `skills/using-superpowers/SKILL.md` 열람)
   - `brainstorming`, `writing-plans`, `test-driven-development`, `systematic-debugging`, `verification-before-completion` 등 15개 스킬 제공.
   - **핵심 관찰**: `using-superpowers/SKILL.md`에서 *"Process skills (`brainstorming`, `systematic-debugging`) come first, then implementation skills"*라는 우선순위를 **산문(prose)**으로 강제하려 하나, 강제 메타데이터나 정적 의존성 그래프·보안 게이트는 없음.
2. **기타 대규모 스킬 디렉터리** (Web Search 확인)
   - `everything-claude-code` (100+ 스킬·훅·에이전트 모음), `travisvn/awesome-claude-skills`, `karanb192/awesome-claude-skills`, `aj-geddes/claude-code-bmad-skills`, `vercel-labs/skills` / `skills.sh`.
   - **공통 한계**: 수십~수백 개 스킬을 평면 리스트로 제공해 스킬 간 위계(Meta → Plan → Execute → Verify), 선행/충돌 규칙, 도메인 분기 격리가 부족함.

## 2. 평면 스킬 모음의 실패 메커니즘 (arXiv 문헌)
- **Skill Shadowing (`arXiv:2605.24050`, Wei et al.)**: 스킬이 수백 개로 늘어나면 컨텍스트 토큰 증가보다 **의미 혼동으로 잘못된 스킬을 고르는 Skill Shadowing**이 20%+ 성능 저하의 주원인.
- **HiSkill (`arXiv:2607.25853`) & HERAKLES (`arXiv:2508.14751`)**: 상위 매크로 스킬과 하위 원자 스킬을 타입 엣지·선행 구조로 연결한 계층 그래프가 모호성과 토큰 비용을 절감.
- **SKILLCLASH**: 충돌하는 규칙이 평면으로 동시 로드되면 모델이 한쪽 스킬을 통째로 덮어쓰고 다른 쪽 규칙을 무시하는 takeover 현상 발생.
- **해결**: 우리 시스템에서는 HTML 분기 트리로 활성 스킬만 노출하고, [`rules/skill-hierarchy.json`](../rules/skill-hierarchy.json) + `order_skill_pipeline()`으로 4계층(`Tier 0 Gate → Tier 1 Plan → Tier 2 Execute → Tier 3 Verify`)과 `requires`/`conflicts_with`를 결정적으로 해결.

## 3. 악성 스킬 공급망 위협 및 방어 체계
- **실태 (Snyk *ToxicSkills*, *Skill-Inject*)**: 공개 에이전트 스킬의 **36%+**에서 보안 결함이 발견되며 **13%–26%**는 심각/악성 페이로드 포함.
- **주요 공격 벡터**:
  1. `SKILL.md` / `references/` 내 간접 프롬프트 인젝션 (`ignore previous instructions`, 은닉 지시)
  2. `.env`, `.ssh/id_*`, `.aws/credentials`, 메모리 파일 탈취 및 외부 웹훅/DNS 유출
  3. `curl | bash` / `Invoke-Expression` 원격 페이로드 실행 및 런타임 자기변조
- **방어 도구 및 적용**:
  - **NVIDIA SkillSpector** 패턴(정적 AST/패턴 스캔 + 인젝션/유출/경로탈출 탐지)을 무의존성 정적 게이트 [`scripts/scan_skills_security.py`](../scripts/scan_skills_security.py)로 구현하고, [`scripts/validate_harness.py`](../scripts/validate_harness.py)가 자동 실행해 차단함.
