---
rule_id: coding.debugging.runtime
parent: "coding.debugging"
depth: 3
title: "런타임 · 로직 버그 수정 (Runtime & Logic)"
html_title: "Runtime Debugging · HTML Branching Rules"
heading: "런타임 · 로직 버그 수정"
tier: mid
effort: medium
skills: [targeted-debug]
pillars: [harness, loop]
keywords: [stack trace, nullpointer, typeerror, keyerror, assertion, unit test, 예외, 스택 트레이스, 로직 버그, 단위 테스트]
escalation_policy: effort-first-with-verifier
workload_profile: verified_coding
escalate_when: ["attempts>=2", "coupled_files>=4"]
---

> 명확한 스택 트레이스나 단위 테스트 실패를 국소 패치로 해결하는 전형적 중위 난이도 말단 분기입니다.

## Rules: 말단 실행 체크리스트
- 오류 발생 라인과 직전 호출부(최대 150라인)만 읽어 입력-상태 불일치를 특정한다.
- 경계값(None/빈 리스트/인코딩/오프바이원)을 검증하는 회귀 테스트를 추가한다.
- 2회 실패 내 미해결, 파일 4+ 결합, 또는 단위 테스트 검증기 부재(Modal Ceiling) 시 동일 모델 Effort 반복 대신 `debugging-concurrency`/`architecture` 상위 모델로 전환한다.
