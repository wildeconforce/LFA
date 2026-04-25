# Module reference

Detailed reference for the 13 LFA modules.

For the high-level architecture and data flow, see
[`ARCHITECTURE.md`](ARCHITECTURE.md).

---

## Track A — Analysis

### Module 1: CASE_SCANNER (`lfa.scanner`)

Parse heterogeneous case-file inputs into a structured `CaseRecord`.

**Input formats:** PDF (text and image), DOCX, HWP/HWPX, plain text.

**Pipeline:**
1. Format detection.
2. Text extraction (pymupdf for PDF text path, pytesseract+kor for
   OCR fallback, python-docx for DOCX, pyhwp for HWP).
3. Korean NER + regex for dates, parties, amounts, case numbers.
4. 6-question structuring (who / when / where / what / how / why).
5. Timeline auto-build with duplicate-event resolution.

**Public API:**
- `scan_case(case_dir) -> CaseRecord`
- `scan_document(path) -> dict`

---

### Module 2: LOGIC_BREAKER (`lfa.breaker`)

Detect weaknesses in the opposing party's claims.

**Weakness types:**
- Temporal contradiction
- Evidence-claim mismatch
- Legal reasoning error
- Statement reversal across briefs
- Self-contradiction within a single party's documents
- **Quotation tampering** — partial-citation distortion of source meaning

**Output:** `BreakerReport` with per-claim findings + a single
`kill_shot`.

**Public API:**
- `break_logic(case, target_party) -> BreakerReport`
- `detect_quotation_tampering(quoted, source_text) -> dict | None`

---

### Module 3: PRECEDENT_HUNTER (`lfa.hunter`)

Search and **cross-verify** Korean Supreme Court precedents and
statutes.

**Verification rule:** every cited 판례 must be confirmed by ≥2 of
4 sources (`law.go.kr` / `casenote.kr` / `bigcase.ai` /
`glaw.scourt.go.kr`). Failed verification → citation deleted.

**Public API:**
- `hunt_precedents(issue_keywords, min_count) -> HunterReport`
- `verify_precedent(case_number) -> (verified, sources)`

---

### Module 4: DOC_WRITER (`lfa.writer`)

Generate a draft legal document.

**Document kinds:** 준비서면 / 답변서 / 내용증명 / 탄원서 / 고소장 초안

**Tone profiles:** `professional` (attorney register) / `human`
(pro se narrative) / `hybrid`

**Mandatory disclaimer footer** auto-appended; cannot be disabled.

**Public API:**
- `write_document(case, kind, tone, breaker?, hunter?, output_path?)
   -> DraftDocument`

---

### Module 5: HUMAN_REVIEW (`lfa.reviewer`)

Capture user feedback and apply corrections.

**Feedback categories:** `fact_error`, `frame_risk`,
`unnecessary_disclosure`, `tone_issue`, `legal_term_risk`,
`contradiction`.

**Public API:**
- `collect_feedback(draft) -> list[FeedbackItem]`
- `apply_feedback(session) -> DraftDocument`

---

### Module 6: FACT_VERIFIER (`lfa.verifier`)

Cross-check every AI-generated claim against source documents.

**Verification categories:** date / quoted_speech / case_number /
case_progression / evidence_number / party_statement.

Returns `VerificationReport` with `safe_to_submit` flag (default
False until affirmatively certified).

**Public API:**
- `verify_draft(draft, case) -> VerificationReport`

---

### Module 7: COUNTER_SIMULATOR (`lfa.simulator`)

Red-team the user's draft from opposing counsel's perspective.

**Strategic principle:** `should_preempt: false` is the default for
every attack vector. The system never volunteers weaknesses the
opposing side has not raised.

**Public API:**
- `red_team(draft, case) -> SimulatorReport`

---

### Module 8: TIMELINE_CONFLICT_DETECTOR (`lfa.timeline`)

Detect chronological contradictions across statements, evidence,
and prior decisions.

**Conflict types:** ordering / duration / simultaneity / existence.

**Public API:**
- `detect_conflicts(case) -> TimelineReport`

---

### Module 14: ADVERSARIAL_LOOP (`lfa.adversarial`)

Closed-loop self-correction + counter-strike. Sits at the end of
the analysis pipeline.

Three sequential operations per iteration:
1. **SELF_AUDIT** — find errors in our own draft (factual / logical /
   tone / unverified citation / internal contradiction / weak phrasing /
   premature concession).
2. **SELF_CORRECT** — apply fixes to the draft.
3. **COUNTER_STRIKE** — re-run weakness detection against the
   opposing brief, but now from the corrected position. The
   **mirror-error principle** applies: error types we made are often
   present on the opposing side too.

**Loop termination:** when `SELF_AUDIT` finds no more must-fix issues
or `max_iterations` is reached.

**Design discipline:** we attack only after we are clean. A draft
with internal errors cannot credibly attack opposing errors — the
opposing side will counter with our own mistakes.

**Public API:**
- `run_loop(draft, case, opposing_brief_text, max_iterations) -> AdversarialReport`
- `self_audit(draft, case) -> list[SelfAuditFinding]`
- `self_correct(draft, findings) -> DraftDocument`
- `counter_strike(revised_draft, opposing_brief_text, case, audit_findings) -> list[CounterStrikeAttack]`

---

## Track B — Simulation (Mock Trial Engine)

### Module 9: PERSONA_LOADER (`lfa.simulation.persona_loader`)

Load synthetic Korean personas from NVIDIA Nemotron-Personas-Korea
into a queryable local SQLite index.

**Roles:** party / judge_1 / judge_2 / attorney / prosecutor / witness.

**Public API:**
- `load_personas(role, count, constraints, seed) -> list[Persona]`
- `build_index(dataset_path, db_path)`

---

### Module 10: CASE_GENERATOR (`lfa.simulation.case_generator`)

Generate fictional Korean cases with asymmetric evidence
distribution.

**Inputs:** issue keywords + plaintiff/defendant personas +
asymmetry_bias (0=balanced, 1=plaintiff-favored).

**Output:** `SyntheticCase` (subclass of `CaseRecord`,
`is_synthetic=true`).

**Public API:**
- `generate_case(config) -> SyntheticCase`

---

### Module 11: MULTI_AGENT_ARENA (`lfa.simulation.arena`)

Round-based multi-agent courtroom simulation.

**Backends:** AutoGen / LangGraph / manual. Each agent's behavior is
parameterized by its persona's style variables.

**Public API:**
- `run_arena(case, plaintiff_counsel, defendant_counsel, ..., max_rounds, backend)
   -> ArenaTranscript`

---

### Module 12: JUDGE_ADJUDICATOR (`lfa.simulation.judge_adjudicator`)

Persona-driven judicial ruling generation.

**Judge axes:** rigor / pace / rationality / precedent_dependence
(each [0, 1]).

The same case + different judge personas → different rulings. That
distribution is the simulator's central output.

**Public API:**
- `adjudicate(transcript, judge) -> Ruling`
- `adjudicate_two_tier(...)` — 1심 → 2심 sequence

---

### Module 13: OUTCOME_ANALYZER (`lfa.simulation.outcome_analyzer`)

Aggregate outcomes across many simulation runs to discover
strategy-vs-judge correlations.

Findings feed back into `LOGIC_BREAKER` (Module 2) as training data
for weakness-detection heuristics. This is the loop that lets the
analysis side improve from simulation evidence.

**Public API:**
- `analyze_outcomes(rulings) -> OutcomeSummary`
- `feedback_to_breaker(summary) -> list[dict]`
