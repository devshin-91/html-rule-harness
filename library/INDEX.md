# Harness² Experience Library (`library/INDEX.md`)

Google Harness² (`google-research/harness2`, arXiv:2610.14224)의 **Harnessing-Level Recursion** 원칙에 따라, 본 프로젝트에서 검증된 하네스 개선 경험과 근거를 축적합니다.

## Entries
- [`EXPERIENCE.md`](./EXPERIENCE.md)
  - **cue**: HTML 규칙 노드 내부에 UI 배지·스타일을 중복 작성해 AI-RULE 블록이 2,800B 상한을 초과할 때
  - **lesson**: AI 컨텍스트 블록(`<!-- AI-RULE-START/END -->`)에는 `data-*` 속성과 핵심 규칙만 남기고, `.rule-eyebrow`/`.rule-badges` 등 인간 UI 요소는 외부 `rule-ui.js`가 동적 하이드레이션하도록 분리한다.
- [`EXPERIENCE.md#iteration-02--03`](./EXPERIENCE.md)
  - **cue**: 분기 트리를 4단계 이상 깊게 쪼개려 할 때 (`arXiv:2607.17598`)
  - **lesson**: 분기 깊이는 Depth 3 이내로 제한하고(`RECOMMENDED_MAX_DEPTH = 3`), `resolve_rule.py`로 단일 XML 패킷 병합 + Cascade Routing(`arXiv:2410.10347`)으로 정확도를 방어한다.
- [`EXPERIENCE.md#iteration-03--04`](./EXPERIENCE.md)
  - **cue**: 도메인 라우터의 자식 분기가 5~6개로 늘어나 AI 블록이 `2,800B`를 초과할 때
  - **lesson**: `<a class="branch-link">` 내부의 중복 `<span>` 설명을 제거하고 `data-tier` 기반 JS 렌더링으로 대체해 라우터 확장성과 컨텍스트 상한을 동시에 지킨다.
- [`EXPERIENCE.md#iteration-04--05`](./EXPERIENCE.md)
  - **cue**: 탐색기 UI에서 수동 트리 클릭과 자동 입력 라우팅이 혼동되거나, CSS Grid에서 코드 패킷이 뷰포트를 뚫고 잘릴 때 / 논증 난이도·Effort 조정이 필요할 때
  - **lesson**: `branchOverride` 시 명시적 수동 탐색 배너 + 복귀 버튼을 노출하고, `min-width: 0`과 `pre-wrap`으로 가로 오버플로우를 원천 차단하며, 논증 역시 `low/mid/high` + 동일 티어 Effort 우선 보정(`28–41`, `60–74`)으로 실증 계층화한다.
- [`EXPERIENCE.md#iteration-05--06`](./EXPERIENCE.md)
  - **cue**: 코딩·RAG·아키텍처 등 작업별로 동일 모델의 Effort만 올릴지, 모델 자체를 바꿀지 결정해야 할 때
  - **lesson**: 4대 정책(`effort-first-with-verifier`, `capacity-switch-sensitive`, `grounding-over-thinking`, `overthinking-guard-low`)과 외부 검증기(`has_verifier`) 유무를 결합해 `raise_effort` vs `switch_model_up` vs `ground_before_think`로 분기한다.
- [`EXPERIENCE.md#iteration-06--07`](./EXPERIENCE.md)
  - **cue**: HTML 분기형 규칙 시스템 + 작업별 모델·Effort 라우팅의 실제 토큰·시간·품질 효용성을 A/B 테스트로 검증하고 쿼터 중단에 대비해야 할 때
  - **lesson**: `benchmark/ab_harness.py`와 체크포인트 캐시(`ab_checkpoint.json`)로 세부 작업 단위 재개를 보장하고, 단일 `<active_rule_packet>` 주입으로 규칙 희석을 차단해 입력 토큰 -33.9%, 총 토큰 -31.3%, 품질 92→100점을 달성한다.
- [`EXPERIENCE.md#iteration-07--08`](./EXPERIENCE.md) & [`experiments/08-v2-md-source-carbon-refactor.md`](./experiments/08-v2-md-source-carbon-refactor.md)
  - **cue**: HTML 수동 편집으로 인한 토큰/diff 오버헤드를 없애고(`md-html-guide`), Gemini 4 Carbon/Argon/Neon/Hydrogen v3.0 스펙과 5계보 Anti-Hallucination 가드레일을 라우터·UI에 통합해야 할 때
  - **lesson**: `rules/src/**/*.md`를 단일 원천으로 두고 `scripts/build_rules_html.py` (`--check`, 0 LLM 토큰)로 28개 HTML 뷰를 결정적 컴파일하며, `resolve_rule.py`는 MD 1순위로 파싱하고 Explorer UI는 JSON/Markdown Export Loop와 `meta.anti-hallucination` 프리셋을 제공한다.

