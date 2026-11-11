# UI/UX Design, Empirical Reasoning Calibration & Commercially-Free Stock Credits

Explorer UI(`rules/index.html`)와 분기 HTML 문서 뷰의 **Anti-Slop 현대화·레이아웃 무결성·인지 부하 저감·논증 Effort 실증 보정**을 위해 참고한 UI/UX 큐레이션·학술 논문 및 적용한 상업적 무료 오픈소스(MIT/ISC/SIL OFL 1.1) 스톡 자산·크레딧 목록입니다.

---

## 1. 적용된 상업적 무료(Commercially Free) 오픈소스 스톡 자산 & 크레딧

| 자산명 | 유형 | 작성자 / 저작권자 | 라이선스 | 적용 위치 및 출처 |
|---|---|---|---|---|
| **Lucide Icons** (`v0.460.0`) | 벡터 UI 아이콘 세트 (28종 SVG 정본 번들) | Lucide Contributors & Cole Bemis (Feather) | **ISC License** / **MIT** (상업적 사용·수정·배포 무료, 저작권 고지 포함) | [`rules/assets/lucide-icons.js`](../rules/assets/lucide-icons.js), [`rules/assets/licenses/lucide-LICENSE.txt`](../rules/assets/licenses/lucide-LICENSE.txt) (`lucide.dev` / jsDelivr CDN) |
| **Pretendard Variable** (`v1.3.9`) | 한글·영문 가변 산세리프 UI 서체 | Kil Hyung-jin (`orioncactus`) | **SIL Open Font License 1.1** (상업적 무료, 단일 폰트 파일 단독 재판매 금지) | [`rules/index.html`](../rules/index.html) CDN + [`rules/assets/licenses/pretendard-OFL.txt`](../rules/assets/licenses/pretendard-OFL.txt) |
| **IBM Plex Sans KR** | 한글·영문 에디토리얼 보조 서체 | IBM Corp. & Sandoll | **SIL Open Font License 1.1** (상업적 무료) | Google Fonts CDN + [`rules/assets/licenses/ibm-plex-OFL.txt`](../rules/assets/licenses/ibm-plex-OFL.txt) |
| **JetBrains Mono** | 코드·XML 패킷·토큰/경로 고정폭 서체 | JetBrains s.r.o. | **SIL Open Font License 1.1** (상업적 무료) | Google Fonts CDN + [`rules/assets/licenses/jetbrains-mono-OFL.txt`](../rules/assets/licenses/jetbrains-mono-OFL.txt) |

> 모든 스톡 자산은 **AI 규칙 본문(`<!-- AI-RULE-START --> ... <!-- AI-RULE-END -->`) 바깥**과 HTML Explorer 쉘에만 적용되어 AI 토큰 절감률(~94~97%)에는 영향을 주지 않습니다.

---

## 2. UI/UX 큐레이션 및 HCI 학술 근거

### A. 웹 UI/UX · 개발자 문서 탐색 모범 사례 (Web Research)
- **Nielsen Norman Group (NN/g) — Progressive Disclosure & Developer UX**: 고빈도 핵심 정보와 드문 고급 설정을 분리해 작업 기억(Working Memory)을 보호하고, 인라인 코드·메타 배지를 뚜렷한 배경/테두리로 본문과 구획화하며 WCAG 고대비 기준을 준수한다.
- **Laws of UX (Jakob's / Hick's / Fitts's / Miller's / Proximity / Tesler's)**:
  - **Jakob's Law**: 좌측 계층 내비게이션, `Ctrl+K` / `/` 검색 포커스, 상단 복사 버튼을 관습 위치에 고정.
  - **Hick's Law & Information Foraging (Pirolli & Card)**: Depth-1 트렁크 아코디언 접기/펼치기 + 검색 필터로 선택 피로를 낮추고, 제목 1줄 + 명확한 티어/토큰 단서로 *Information Scent* 유지.
  - **Fitts's Law**: XML 패킷 상단 헤더에 큼직한 복사 버튼을 배치하고, 트리 수동 선택 시 즉시 `[자동 라우팅 복귀]` 버튼을 제공해 상태 오인을 제거.
- **현대적 에디토리얼 디자인 시스템 참고**: Stripe Docs, Linear, Vercel Geist, Refactoring UI의 **미드톤 따뜻한 페이퍼(`#F6F5F0`) + 고가독 잉크(`#1B1D21`) + Forest Teal(`#0F766E`)** 조합으로 기존 다크 인디고/바이올렛 AI Slop 클리셰를 제거.

### B. Liner Scholar 탐색 HCI & 추론 Effort 실증 논문 (5차 세션)
1. **Forsey et al. (2024)** — *Designing for Learnability: Improvement Through Layered Interfaces* (`DOI: 10.1177/10648046241273291`): 단계적 Progressive Disclosure는 탐색 오류와 학습 분산을 줄이나, 장기 탐색성을 위해 검색·전체 트리 열람 경로를 함께 열어 두어야 함 → **접이식 Depth-1 트리 + 실시간 필터 겸용**.
2. **Springer & Whittaker (2019)** — *Progressive disclosure: empirically motivated approaches to designing effective transparency* (ACM CHI, `DOI: 10.1145/3301275.3302322`): 과도하게 파편화된 다층 공개는 오히려 멘탈 모델을 깨뜨림 → **트리(탐색) + 워크벤치(조정·결과) 2-영역 통합 및 커스텀 빌더 접힘 처리**.
3. **Sweller & Chandler — Cognitive Load Theory (Element Interactivity)**: 파일 수·실패 횟수·동시성·모호성처럼 상호작용하는 변수들은 한 화면(WorkBench)에 통합 배치해 불필요한 시선 분산을 줄임.
4. **Pu et al. (2025)** — *THOUGHTTERMINATOR* (`arXiv:2504.13367`) & **Wu et al. (2025)** — *When More is Less* (`arXiv:2502.07266`) & **Caldarella et al. (2026)** — *Thinking Past the Answer* (`arXiv:2606.02835`):
   - **역-U자 곡선 실증**: 단순 논증(3줄 장단점 요약)은 과잉 CoT가 오히려 정답을 뒤집으므로 `low / effort:low`가 최적.
5. **Kleinman et al. (2025)** — *e1: Learning Adaptive Control of Reasoning Effort* (`arXiv:2510.27042`):
   - 문제 난이도에 따라 티어 상향 전에 **동일 티어 내부 Effort(`low→medium`, `medium→high`) 우선 조정** 적용.
6. **Wang et al. (EMNLP 2023 Findings, `arXiv:2305.13160`)**, **Kim & Khashabi (2025)** (`arXiv:2509.16533`), **Lacombe et al. (2025)** (*Don't Think Twice!*, `arXiv:2508.15050`):
   - **논증 예외 검증**: 반론/재반박·찬반 균형 논증에서 하위 모델은 아첨(sycophancy)과 논리 비약을 보이며, 내부 추론 토큰 증가만으로는 사실 확신 보정이 `48.7%`로 추락함(검색 그라운딩 병행 시 `89.3%`). 따라서 **`reasoning.structured-argument` (`mid`) 분기를 신설**하고 `claim-verify` 그라운딩을 강제함.
