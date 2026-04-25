# LFA v0 PoC — Synthetic Case End-to-End Run

> **Purpose.** Show what each LFA module would output when given a
> realistic synthetic Korean civil/criminal case. Modules are still
> skeletons in v0; this document presents what their *intended*
> output looks like when manually executed by an analyst following
> the module specs.
>
> **Synthetic data.** Every name, case number, date, address, and
> amount in this document is fictional. Any resemblance to real
> persons or cases is coincidental.
>
> **Disclaimer.** This is research output, not legal advice.

---

## 0. Synthetic case input

A fictional 약정금 + 협박 case generated for this PoC. Generated via
direct LLM synthesis (Source 3 in `docs/SYNTHETIC_DATA.md`).

```yaml
case_id: "2024가단99999 약정금"
case_type: "약정금"
court: "서울서부지방법원 (가상)"

parties:
  plaintiff:
    name: "박지훈"  # synthetic
    role: "plaintiff"
    age: 38
    region: "서울 마포구"
    occupation: "카페 운영"
    family: "기혼·자녀1"
  defendant:
    name: "정민수"  # synthetic
    role: "defendant"
    age: 41
    region: "경기 부천시"
    occupation: "주식 트레이더 (자동매매 봇 운용)"
    family: "기혼·자녀2"

claim_amount_krw: 48_000_000
# 5,000만원 송금 - 200만원 변제 = 4,800만원 청구

timeline:
  - "2022-03-15: 정민수가 박지훈에게 자동매매 봇 투자 권유. '5천만원 넣으면 1년 안에 7천만원 만들어준다, 원금 보장'."
  - "2022-03-20: 박지훈이 정민수에게 5,000만원 송금 (계좌이체, 갑제1호증)."
  - "2022-04~06: 봇 운용 보고 카톡 왕래 (수익 +4%, +7%, +2%)."
  - "2022-07-08: 봇 운용 손실. 잔액 3,700만원으로 감소."
  - "2022-09-15: 잔액 1,200만원."
  - "2022-11-02: 정민수가 박지훈에게 손실 공지 (을제2호증 카톡)."
  - "2023-01-10: 박지훈이 원금 반환 요구."
  - "2023-02-05: 박지훈이 정민수에게 협박 메시지 1차. '내 친구들이 너 카페 알고 있다.' (을제3호증)"
  - "2023-02-22: 박지훈 협박 2차. '와이프한테 전화한다.' (을제4호증)"
  - "2023-03~05: 추가 협박 메시지 9회 (을제5~13호증, 시간순)."
  - "2023-06-05: 정민수가 박지훈에게 200만원 송금 (1차 변제, 갑제2호증)."
  - "2023-07-20: 박지훈 약정금 4,800만원 청구 (1심 소장 접수)."
  - "2024-03-15: 1심 청구 기각, 정민수 승소 (1심 판결문, 을제14호증)."
  - "2024-04-10: 박지훈 항소."
  - "2024-10-20: 정민수가 박지훈을 협박죄로 형사고소."
  - "2025-05-30: 박지훈 협박죄 유죄 확정 (서울서부지법 2024고정XXX, 벌금 80만원, 집유 1년) (을제15호증)."
  - "2026-04 현재: 항소심 진행 중."

evidence:
  plaintiff_side:
    - "갑제1호증: 5,000만원 계좌이체 내역"
    - "갑제2호증: 200만원 입금 내역"
    - "갑제3호증: 2022-03-15 카톡 (원금보장 약정 주장의 근거)"
  defendant_side:
    - "을제1호증: 자동매매 봇 운용 일지"
    - "을제2호증: 2022-11-02 손실 공지 카톡"
    - "을제3~13호증: 박지훈 협박 메시지 11건 (시간순)"
    - "을제14호증: 1심 판결문"
    - "을제15호증: 박지훈 협박죄 유죄 확정 형사판결문"

opposing_brief_text_excerpt: |
  ... 피고는 2022. 3. 15. 원고에게 자동매매 봇으로 1년 안에 7천만원을
  만들어주겠다고 약속하면서 원금을 보장하였습니다. 원고는 이를 신뢰하여
  5,000만원을 송금하였으나 피고는 이를 변제하지 않고 있습니다. 피고가
  2023. 6. 5. 200만원을 송금한 사실 자체가 본 약정의 존재를 인정하는
  것입니다 ...
```

---

## 1. CASE_SCANNER (Module 1)

For a synthetic case generated as structured YAML, scanning is a
no-op identity transform. Output: a `CaseRecord` matching the input.

```python
case = CaseRecord.parse_obj(synthetic_case_yaml)
# case.case_id = "2024가단99999 약정금"
# case.timeline = [16 events]
# case.parties = 2
# case.evidence = 14 items (3 갑호증 + 11 을호증)
# case.prior_decisions = [1 civil + 1 criminal]
```

For real PDF/HWP inputs, this is where OCR + Korean NER would run.

---

## 2. TIMELINE_CONFLICT_DETECTOR (Module 8)

**Input:** `case` from §1.

**Detected conflicts:** 0 critical, 1 material.

```yaml
conflicts:
  - event_a: "2022-03-15: 원금보장 약정 주장 (원고 측)"
    event_b: "2022-11-02: 손실 공지 카톡 (피고가 손실 사실 자유롭게 알림)"
    contradiction_type: "existence"
    severity: "material"
    description: |
      원금보장 약정이 존재했다면, 피고가 손실 사실을 원고에게 자발적으로
      공지(2022-11-02)할 동기가 약함. 약정이 있었다면 손실은 피고
      개인의 부담이지 원고에게 알릴 사항이 아님. 손실을 자발적으로
      알린 행위 자체가 "투자에 따른 결과 공유"의 패턴이지,
      "약정 채무자의 변제 회피" 패턴이 아님.

favorable_arrangement:
  - "2022-03-15: 원고가 피고의 봇 운용 실적을 보고 자발적으로 투자 결정"
  - "2022-04~06: 수익기 — 양측 정상 소통"
  - "2022-07~09: 손실기 — 피고가 손실을 자발적으로 공지 (자유 의사 동반자 패턴)"
  - "2023-01: 원고가 손실 회복 안 됨에 따라 원금 반환 요구 시작"
  - "2023-02~05: 원고의 협박 시작 — 외포상태 진입"
  - "2023-06: 피고가 협박에 굴복하여 200만원 송금"
  - "2024-03: 1심 기각"
  - "2025-05: 협박죄 유죄 확정"

notes:
  - "2023-06-05 200만원 송금이 원고측 약정 인정 증거가 아니라 피고의 외포상태에 의한 굴복 송금임을 시간순으로 보여줌."
```

---

## 3. PRECEDENT_HUNTER (Module 3)

**Input:** issue keywords `["강박에 의한 의사표시", "협박죄", "확정 형사판결의 민사 증거력"]`.

**Output (verified ≥2 of 4 sources, hallucination check):**

```yaml
precedents:
  - case_number: "97다24276"
    court: "대법원"
    date: "1997-09-30"
    summary: "확정된 형사판결이 유죄로 인정한 사실은 유력한 증거자료가 되므로, 민사재판에서 특별한 사정이 없는 한 이와 반대되는 사실은 인정할 수 없다."
    verified: true
    verification_sources: ["law_go_kr", "casenote", "glaw_scourt"]
    relevance: "박지훈 협박죄 유죄 확정 → 민사 항소심에서 협박 사실 인정 강제."

  - case_number: "95다1460"
    court: "대법원"
    date: "1996-10-11"
    summary: "강박의 정도가 극심하여 의사결정의 자유가 완전히 박탈된 경우 의사표시는 무효이며, 그렇지 않더라도 민법 제110조에 의해 취소 가능."
    verified: true
    verification_sources: ["law_go_kr", "glaw_scourt"]
    relevance: "2023-06-05 200만원 송금이 협박 외포상태에서 이루어진 것이라면 무효 또는 취소 대상."

  - case_number: "96다9621"
    court: "대법원"
    date: "1996-05-28"
    summary: "확정 형사판결의 사실인정은 민사재판에 있어서 유력한 증거가 됨."
    verified: true
    verification_sources: ["law_go_kr", "casenote"]
    relevance: "97다24276과 동일 법리, 형사판결 사실인정 효력 강조."

# 1개 누락된 후보 — 검증 실패 (가상)
# rejected:
#   - case_number: "2018다99999" — 단 1개 소스에서만 발견, 2-of-4 미달
#     → 인용 금지

statutes:
  - law: "민법"
    article: "제110조"
    content: "사기나 강박에 의한 의사표시는 취소할 수 있다."
    verified: true
  - law: "형법"
    article: "제283조 제1항"
    content: "사람을 협박한 자는 3년 이하의 징역, 500만원 이하의 벌금, 구류 또는 과료에 처한다."
    verified: true
```

검증 실패한 1개는 출력에서 제거됨 (hallucination 0).

---

## 4. LOGIC_BREAKER (Module 2) — 첫 번째 패스

**Input:** `case` + `target_party = plaintiff`

**Output:**

```yaml
findings:
  - claim: "피고가 2023. 6. 5. 200만원을 송금한 사실 자체가 본 약정의 존재를 인정하는 것입니다."
    weakness_kind: "evidence_claim_mismatch"
    weakness_description: |
      이 송금은 협박 메시지 11회(2023-02~05)가 누적된 직후 이루어짐. 송금 시점이 협박 시간선과 직접 연결됨. 약정 인정의 행동이 아니라 외포에 의한 굴복 송금임이 시간순으로 입증.
    counter_argument: |
      형사판결 확정 사실(원고가 협박죄 유죄)에 비추어, 협박 직후 송금은 강박에 의한 의사표시이며, 민법 제110조에 의해 취소 가능하거나, 95다1460에 따라 무효임.
    supporting_evidence: ["을제3~13호증 협박 메시지 11건", "을제15호증 형사 유죄 확정 판결문"]
    strength: "very_strong"

  - claim: "원금보장 약정이 있었습니다."
    weakness_kind: "evidence_claim_mismatch"
    weakness_description: |
      원금보장 약정의 객관적 자료(서면, 계약서, 카톡 명시 발언)가 갑제3호증 외에 없음. 갑제3호증 자체는 "1년 안에 7천만원 만들어주겠다"는 수익 약속이지, "손실시 원금 보장"의 명시적 약정이 아님.
    counter_argument: |
      카톡 본문에 "원금 보장"이라는 명시 표현이 있는지 확인 필요. 만약 "1년 안에 7천만원"만 언급되어 있다면, 이는 수익 예상치이지 보장 약정이 아님.
    supporting_evidence: ["갑제3호증 카톡 원본 본문"]
    strength: "strong"

  - claim: "피고는 변제하지 않고 있습니다."
    weakness_kind: "self_contradiction"
    weakness_description: |
      원고측 본인이 "2023. 6. 5. 200만원을 송금" 사실을 인정. 그렇다면 "변제하지 않고 있다"는 표현은 부정확. "전부 변제하지 않았다" 또는 "잔여 변제 미완"이 정확.
    counter_argument: |
      원고측 표현 자체에서 모순. 본 사건 청구액 4,800만원은 5,000만원 - 200만원이므로, 원고도 200만원 변제 사실은 인정. 그러나 그 200만원은 협박 후 굴복 송금이지 약정 이행이 아님.
    supporting_evidence: ["원고 청구취지", "을제3~13호증"]
    strength: "medium"

kill_shot: |
  원고가 약정 인정 증거로 내세우는 모든 사실(2023-06-05 200만원 송금, 갑제3호증 카톡)은 모두 협박 시간선의 영향권 안에서 발생하거나 약정 본문에 "원금 보장" 명시 발언이 없음. 그리고 원고는 본 사건 동일 사실관계로 협박죄 유죄가 확정됨. 형사판결 인정사실(97다24276)과 강박 의사표시 효력(95다1460)을 결합하면, 원고가 약정 증거로 제시하는 사실들은 본 민사 청구의 근거가 될 수 없음.
```

---

## 5. DOC_WRITER (Module 4) — v1 초안

**Input:** `case` + `breaker_report` + `hunter_report`

**Output:** 준비서면 v1 초안 (피고측, hybrid 톤). 약 800자 본문.

```markdown
# 준비서면 v1

사건: 2024가단99999 약정금
원고(항소인): 박지훈
피고(피항소인): 정민수

1. 사실관계 정리

피고는 2022. 3. 20. 원고로부터 5,000만원을 자동매매 봇 운용 자금으로
받았습니다. 봇 운용 결과 손실이 발생하였고, 피고는 2022. 11. 2. 손실
사실을 원고에게 자발적으로 공지하였습니다.

2023. 1. 10. 원고가 원금 반환을 요구하기 시작한 직후인 2023. 2. 5.부터
약 4개월간 원고는 피고에게 11회에 걸쳐 협박 메시지를 발송하였습니다
(을제3~13호증). "내 친구들이 너 카페 알고 있다", "와이프한테 전화한다"
등의 내용입니다.

이러한 협박이 누적된 직후인 2023. 6. 5. 피고는 200만원을 원고에게
송금하였습니다.

원고는 본 사건과 동일한 협박 사실관계로 형사고소 당하였고,
2025. 5. 30. 협박죄 유죄가 확정되었습니다 (을제15호증).

2. 1심 판결의 정당성

1심은 원금보장 약정의 객관적 증거가 부족하다는 이유로 원고 청구를
기각하였습니다. 이는 정당한 판단입니다.

3. 강박에 의한 의사표시 — 200만원 송금의 효력

원고가 약정 인정의 증거로 내세우는 2023. 6. 5. 200만원 송금은,
원고의 협박이 누적된 외포상태에서 이루어진 것입니다.

대법원은 강박의 정도가 극심하여 의사결정의 자유가 완전히 박탈된 경우
의사표시는 무효이며, 그렇지 않더라도 민법 제110조에 의해 취소할 수
있다고 판시하였습니다 (대법원 1996. 10. 11. 선고 95다1460 판결).

4. 형사 유죄 확정 판결의 민사 증거력

대법원은 확정된 형사판결이 유죄로 인정한 사실은 민사재판에서 유력한
증거자료가 된다고 판시하였습니다 (대법원 1997. 9. 30. 선고 97다24276
판결, 1996. 5. 28. 선고 96다9621 판결).

원고의 협박은 형사판결로 확정되었으므로, 본 항소심은 협박 사실을
사실인정의 토대로 받아들여야 합니다.

5. 결론

원금보장 약정의 증거는 부족하고, 약정 인정의 유력 증거로 제시된
200만원 송금은 협박에 의한 무효 또는 취소 대상입니다. 원심의 판단은
정당합니다.

원고의 항소를 기각하여 주시기 바랍니다.

---

본 내용은 법률적 조언이 아닌 전략적 참고 자료입니다. 실제 소송 행위
시에는 반드시 변호사 또는 법무사의 검토를 거치시기 바랍니다.
```

---

## 6. FACT_VERIFIER (Module 6)

**Input:** `draft_v1` + `case`

**Output:**

```yaml
conflicts: []
safe_to_submit: false  # 아직 ADVERSARIAL_LOOP 통과 전
warnings:
  - category: "quoted_speech"
    excerpt: "내 친구들이 너 카페 알고 있다"
    note: "협박 메시지 원문 11건 중 첫 번째 메시지에서 추출. 다른 메시지의 더 결정적 표현이 있는지 검토 필요."
    severity: "info"
action_required: "ADVERSARIAL_LOOP 통과 후 재확인."
```

---

## 7. COUNTER_SIMULATOR (Module 7)

**Input:** `draft_v1` + `case`

**Output:** 상대방 변호사 입장에서 본 v1 공격 벡터 5개.

```yaml
attack_vectors:
  - target: "§3 강박에 의한 의사표시 — 200만원 송금의 효력"
    attack: |
      "협박이 4개월간 누적된 직후 송금했다는 시간순 입증이 약함. 협박 메시지 11건의 시간 분포가 균등하지 않다면, 마지막 협박과 송금 사이의 시간 간격이 길 경우 외포상태 단절 주장이 가능."
    risk_level: "high"
    should_preempt: true
    note: "11건의 정확한 시간 분포를 v1에 명시하면 더 강함."

  - target: "§1 사실관계 정리 — '봇 운용 결과 손실'"
    attack: |
      "손실의 구체 원인(봇 알고리즘 결함? 시장 변동? 피고의 무능?)이 불명확. 피고의 과실 또는 의도적 부실 운용 가능성 제기 가능."
    risk_level: "medium"
    should_preempt: false
    note: "상대가 안 건드린 영역 — 먼저 꺼내지 말 것."

  - target: "§2 1심 판결의 정당성"
    attack: |
      "1심 판결문 본문 인용 없이 '정당하다'고만 주장. 1심이 어떤 사정을 종합했는지 본문 인용 없으면 약함."
    risk_level: "medium"
    should_preempt: true

  - target: "§4 형사 유죄 확정"
    attack: |
      "형사판결 양형 부분에서 집행유예가 선고됐다는 점을 원고측이 narrative로 활용 가능 — '재판부도 사정을 참작했다.' 양형이유 원문을 미리 인용해 둘 필요."
    risk_level: "high"
    should_preempt: true

  - target: "전반"
    attack: |
      "v1은 '원금보장 약정의 부재'를 적극 입증하지 않음. 갑제3호증 카톡 본문에 '원금 보장' 명시 발언이 없다는 사실을 본문 인용으로 박지 않음."
    risk_level: "high"
    should_preempt: true

overall_risk: "medium"
```

---

## 8. ADVERSARIAL_LOOP (Module 14) — 핵심

이 모듈이 PoC의 하이라이트. 위 모든 분석을 받아 자체 검증 + 상대 역공.

### 8a. SELF_AUDIT (반복 1)

```yaml
findings:
  - category: "weak_phrasing"
    location_excerpt: "이러한 협박이 누적된 직후인 2023. 6. 5. 피고는..."
    issue: |
      "누적된 직후" 표현은 모호. 마지막 협박과 200만원 송금 사이의 정확한 시간 간격이 명시되어 있지 않아 외포상태 지속 입증이 약함.
    suggested_fix: |
      "원고의 협박 메시지 11건은 2023. 2. 5.부터 2023. 5. 28.까지 발송되었고, 마지막 협박 메시지 발송일로부터 8일 후인 2023. 6. 5. 피고는 200만원을 송금하였습니다."
    severity: "must_fix"

  - category: "premature_concession"
    location_excerpt: "1심 판결의 정당성"
    issue: |
      1심 판결문 본문을 인용하지 않고 "정당하다"고만 함. 1심 판결문이 어떤 사정을 종합했는지 본문 인용을 박는 것이 더 강함.
    suggested_fix: |
      1심 판결문 결정적 인용 추가: "원금보장을 약속하였다는 객관적 자료가 일절 없는 점, 피고가 받은 자금을 실제로 자동매매 봇에 사용한 점 등을 종합하여..."
    severity: "must_fix"

  - category: "factual_error"
    location_excerpt: "갑제3호증 카톡 본문에 '원금 보장' 명시 발언"
    issue: |
      v1에서는 갑제3호증 카톡 본문 자체를 인용하지 않음. 카톡 본문에 "원금 보장" 표현이 있는지 명시적으로 다루지 않으면 원고측이 carry할 가능성.
    suggested_fix: |
      "갑제3호증 카톡 본문은 '1년 안에 7천만원'이라는 수익 예상 표현만 포함하고 있을 뿐, '손실시 원금 보장'의 명시적 약정 표현이 존재하지 않습니다."
    severity: "must_fix"

  - category: "unverified_citation"
    location_excerpt: "(대법원 1996. 5. 28. 선고 96다9621 판결)"
    issue: |
      96다9621은 PRECEDENT_HUNTER에서 검증되었으나, draft에 추가 1개 소스 명시(`verification_sources: 2`)가 권장됨.
    suggested_fix: "(별도 변경 불필요, FACT_VERIFIER가 OK)"
    severity: "nice_to_have"

  - category: "tone_problem"
    location_excerpt: "원고의 항소를 기각하여 주시기 바랍니다."
    issue: "결론이 너무 짧음. 정리 단락 추가 권장."
    suggested_fix: |
      결론 단락 보강: "이 사건의 사실관계는 (1) 원금보장 약정의 객관 증거 부재, (2) 200만원 송금은 협박 외포상태에서 발생, (3) 협박은 형사판결로 확정으로 정리됩니다. 따라서..."
    severity: "must_fix"

initial_findings_count: 5  # (must_fix 4 + nice_to_have 1)
```

### 8b. SELF_CORRECT (반복 1)

위 5개 finding 적용 → `draft_v2`. 본문 약 1,200자로 증가.

### 8c. SELF_AUDIT (반복 2)

```yaml
findings: []  # 모든 must_fix 적용 완료
final_findings_count: 0
converged: true
iterations_run: 2
```

### 8d. COUNTER_STRIKE (clean position에서)

이제 v2가 깨끗하니 상대 측 약점에 역공:

```yaml
counter_strikes:
  - target_excerpt: "피고는 2022. 3. 15. ... 원금을 보장하였습니다."
    attack: |
      원고는 원금보장 약정의 명시적 표현이 갑제3호증 어디에 있는지 본문 인용으로 입증해야 합니다. 갑제3호증 카톡 본문은 "1년 안에 7천만원"이라는 수익 예상치이지, "손실시 원금 보장"의 약정이 아닙니다. 수익 예상과 원금 보장은 법적으로 다른 개념입니다.
    grounding: ["갑제3호증 카톡 원본 본문", "1심 판결문의 동일 판단"]
    priority: "killshot"
    mirror_of: null  # 상대측의 발췌 회피 패턴

  - target_excerpt: "피고가 2023. 6. 5. 200만원을 송금한 사실 자체가 본 약정의 존재를 인정하는 것입니다."
    attack: |
      이 송금은 협박 메시지 11건이 발송된 직후(마지막 협박일로부터 8일 후) 이루어진 것이며, 원고의 협박은 본 사건과 동일한 사실관계로 형사 유죄 확정되었습니다. 약정 인정 행위가 아니라 강박에 의한 의사표시이며, 민법 제110조 및 대법원 95다1460에 의해 취소 또는 무효 대상입니다.
    grounding: ["을제3~13호증 협박 메시지 11건", "을제15호증 형사 유죄 확정", "민법 제110조", "대법원 95다1460"]
    priority: "killshot"
    mirror_of: "weak_phrasing in our v1"

  - target_excerpt: "피고는 ... 변제하지 않고 있습니다."
    attack: |
      원고 본인이 청구취지에서 5,000만원이 아닌 4,800만원을 청구함. 즉 원고도 200만원 변제 사실은 인정. "변제하지 않고 있다"는 표현은 자기모순. 그리고 그 200만원은 위 §3-나에서 본 바와 같이 협박에 의한 굴복 송금임.
    grounding: ["원고 청구취지 본문", "본 답변서 §3-나"]
    priority: "high"
    mirror_of: "self_contradiction principle"

  - target_excerpt: "원고는 이를 신뢰하여 5,000만원을 송금하였으나..."
    attack: |
      원고가 신뢰의 기초로 삼았다는 약정 표현이 갑제3호증 어디에 있는지 본문 인용 없음. 신뢰의 기초가 되는 약정 표현이 없으면 신뢰의 정당성 자체가 입증되지 않음.
    grounding: ["갑제3호증 카톡 원본"]
    priority: "high"
    mirror_of: "factual_error in our v1"

overall_assessment: |
  v2 (clean draft) 위치에서 본 상대 약점:
    1. 약정의 명시적 표현 부재 (kill_shot 강함)
    2. 200만원 송금의 강박 무효/취소 가능성 (killshot 강함)
    3. 청구취지 자체의 자기모순 (high)
    4. 신뢰 기초의 부재 (high)
  → 모든 공격은 V2 본문에 이미 반영된 사실/판례에 grounded 되어 있음.
  → should_preempt 결정은 전략 단계에서 결정 (이 PoC에서는 전체 expose).
```

### 8e. 최종 산출 — `draft_v2` + counter-strikes 반영 권고

```yaml
adversarial_report:
  iterations_run: 2
  initial_findings_count: 5
  final_findings_count: 0
  converged: true
  counter_strikes_count: 4  # 2 killshot + 2 high
  final_draft_length_chars: 1240
  safe_to_submit: true
  notes:
    - "v1의 5개 must-fix를 1차 반복에 모두 해결, 2차 반복에서 추가 finding 0."
    - "Mirror-error principle로 v1의 weak_phrasing이 상대측의 동일 패턴 발견에 도움됨 (counter_strike #2)."
    - "Mirror-error principle로 v1의 factual_error가 상대측 신뢰 기초 부재 발견에 도움됨 (counter_strike #4)."
```

---

## 9. JUDGE_ADJUDICATOR (Module 12) — 가상 판사 시뮬레이션

위 v2 + counter-strikes를 4개 다른 기질의 합성 판사 페르소나에 입력.

### Judge profile A — 꼼꼼·법리·판례의존
```yaml
rigor: 0.9
pace: 0.3
rationality: 0.9
precedent_dependence: 0.9
ruling: "plaintiff_loss"
reasoning_summary: |
  형사 확정 판결의 사실인정 효력 (97다24276) + 강박 의사표시 (95다1460)
  결합으로 200만원 송금 효력 부정. 약정의 명시적 증거 부재. 항소 기각.
```

### Judge profile B — 보통속도·균형·문헌의존
```yaml
rigor: 0.7
pace: 0.5
rationality: 0.6
precedent_dependence: 0.7
ruling: "plaintiff_loss"
reasoning_summary: |
  1심 판단 정당. 형사 유죄 확정 사실 + 약정 명시 증거 부재. 항소 기각.
```

### Judge profile C — 빠름·감성·즉시판단
```yaml
rigor: 0.4
pace: 0.8
rationality: 0.3
precedent_dependence: 0.4
ruling: "plaintiff_partial"
reasoning_summary: |
  형사 유죄는 인정하나, 동대문/마포 카페업의 어려운 사정도 일부 참작.
  일부 인용 (예: 200만원 한정).
```

### Judge profile D — 매우 꼼꼼·매우 신중·법리
```yaml
rigor: 1.0
pace: 0.1
rationality: 1.0
precedent_dependence: 1.0
ruling: "plaintiff_loss"
reasoning_summary: |
  Judge A와 유사하나 더 상세 인용. 항소 기각.
```

### Outcome distribution

| Judge profile | Ruling | Notes |
|---|---|---|
| A (꼼꼼·법리) | plaintiff_loss | 강한 기각 |
| B (균형) | plaintiff_loss | 표준 기각 |
| C (감성·빠름) | plaintiff_partial | 200만원 인용 (일부) |
| D (매우 꼼꼼) | plaintiff_loss | 가장 강한 기각 |

**75%는 완전 기각, 25%는 일부 인용**. PoC는 v2 brief가 75% 강한 기각을 끌어낼 수 있는 위치에 있음을 보여줌.

---

## 10. OUTCOME_ANALYZER (Module 13)

```yaml
total_simulations: 4
by_outcome:
  plaintiff_loss: 3
  plaintiff_partial: 1
  plaintiff_full_win: 0

notable_correlations:
  - "Higher rigor + higher precedent_dependence → stronger 기각."
  - "Lower rationality (감성형 판사)는 일부 인용 가능성."
  - "200만원 강박 무효 주장이 모든 판사 기질에서 효과적."

feedback_to_breaker:
  - pattern: "수익 예상 vs 원금 보장 구분 missing → 항상 본문 인용으로 박을 것"
  - pattern: "협박 시간선과 송금 시간 차이 명시 → 모든 판사 기질에 효과적"
```

---

## 11. 종합 평가

이 PoC는 LFA의 14개 모듈이 **합성 케이스 1건에 대해 어떤 결과를 산출하는지** 단계별로 보여줍니다.

핵심 검증 포인트:

| 모듈 | PoC에서 보인 가치 |
|------|-------------------|
| 1. CASE_SCANNER | 합성 케이스 그대로 통과 (real-PDF parse는 추후) |
| 2. LOGIC_BREAKER | 약점 3개 + kill_shot 1개 식별 |
| 3. PRECEDENT_HUNTER | 3 판례 검증 통과, 1개 검증 실패로 제거 (hallucination 0) |
| 4. DOC_WRITER | 800자 v1 초안 생성 |
| 5. HUMAN_REVIEW | (이 PoC는 자동 모드, HUMAN_REVIEW 생략) |
| 6. FACT_VERIFIER | v1 통과, ADVERSARIAL_LOOP 후 재검증 |
| 7. COUNTER_SIMULATOR | 5 attack vectors, should_preempt 분기 |
| 8. TIMELINE_DETECTOR | 1 material conflict 발견 (favorable_arrangement 도출) |
| 9-13. Mock Trial | 4 판사 기질 시뮬, 75% strong-kick 분포 |
| **14. ADVERSARIAL_LOOP** | **5 self-audit findings → v2 보강 → 4 counter-strikes (2 killshot + 2 high)** |

**Module 14가 PoC의 가장 큰 가치 — 자기 검증 후 깨끗한 위치에서 역공.**
v1을 그대로 제출했다면 `weak_phrasing`, `premature_concession`, `factual_error` 3개가 그대로 노출되어 상대가 카운터할 가능성이 컸음. ADVERSARIAL_LOOP가 이를 사전 차단하고, 동시에 mirror-error principle로 상대 약점 2개(#2, #4)를 추가 발굴함.

---

## 12. 한계 및 다음 단계

이 PoC는 **수동 시뮬레이션**입니다. 실제 작동 코드는 아직 v0 skeleton 상태이며, 다음 마일스톤에서 LLM-backed 실제 구현이 들어갑니다:

- v0.1: CASE_SCANNER + LOGIC_BREAKER + DOC_WRITER 실제 LLM 백엔드 연결
- v0.2: PRECEDENT_HUNTER 4-source 검증 실제 스크래퍼/API
- v0.3: 합성 케이스 fixture 자동 생성 (Nemotron 통합)
- v0.4: Mock Trial Engine 실제 멀티에이전트
- v1.0: 14개 모듈 모두 작동 + 회귀 테스트

이 문서 자체가 **각 모듈의 출력 contract** 역할 — 구현이 들어올 때 이 모양과 일치해야 함.

---

본 내용은 법률적 조언이 아닌 전략적 참고 자료입니다. 실제 소송 행위
시에는 반드시 변호사 또는 법무사의 검토를 거치시기 바랍니다.

This output is strategic reference material only, not legal advice.
Review by a licensed attorney or 법무사 is required before any
reliance on this output for litigation purposes.

---

*Generated by LFA v0 — manual module execution against synthetic case.*
*Synthetic case is fictional. Any resemblance to real persons or cases is coincidental.*
