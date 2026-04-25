# Safety contract

LFA enforces non-negotiable safety properties. These are the rules
the framework imposes on every output and every contributor.

## 1. Zero-hallucination on precedents

Every Korean Supreme Court precedent (`판례`) cited in any output —
brief, demand letter, summary — must be confirmed by **at least 2
of the following 4 sources**:

1. 국가법령정보센터 (`law.go.kr`)
2. CaseNote (`casenote.kr`)
3. BigCase (`bigcase.ai`)
4. 대법원 종합법률정보 (`glaw.scourt.go.kr`)

The verification gate lives in `lfa.hunter.verify_precedent()`.
Code paths that bypass `verify_precedent` and emit a `case_number`
into a draft are in violation of this contract.

Target hallucination rate: **0%**. Citations that fail verification
are deleted, not generated.

## 2. Mandatory disclaimer

Every generated document carries the disclaimer footer:

> 본 내용은 법률적 조언이 아닌 전략적 참고 자료입니다.
> 실제 소송 행위 시에는 반드시 변호사 또는 법무사의 검토를
> 거치시기 바랍니다.

The disclaimer is appended automatically by `lfa.writer.write_document`
and **cannot be disabled** via configuration.

## 3. PII redaction at every boundary

Anything leaving LFA's process boundary (logs, exports, shared
documents, simulation outputs) must pass through `lfa.utils.redactor.redact()`
first. Patterns redacted:

- 주민등록번호 (resident registration numbers)
- Phone numbers
- Bank account numbers
- Korean names (heuristic; conservative)
- Addresses (street level)
- Case numbers (when `context="publish"`)

Automated redaction is a first pass. Sensitive outputs (anything
intended for publication, social media, or a third party) require
human review before release.

## 4. No real-case material in the repository

The `data/synthetic/` directory holds **only** generated synthetic
fixtures. Any commit containing real-case material (real names, real
case numbers, real party communications) must be reverted before
being merged.

The `.gitignore` enforces this for common patterns. Contributors who
add new file naming conventions for case material must update
`.gitignore` in the same PR.

## 5. Simulation outputs are not legal advice

Outputs from the Mock Trial Engine (Modules 9–13) are explicitly
marked `is_synthetic: true`. They are research artifacts, not
predictions of real-court outcomes. They must not be used to advise
parties on whether to settle, appeal, or submit any specific document.

## 6. Defensive defaults

- `should_preempt: false` is the default for every attack vector
  surfaced by `COUNTER_SIMULATOR`. The system does not volunteer
  weaknesses the opposing party has not raised.
- `safe_to_submit: false` is the default until `FACT_VERIFIER`
  affirmatively certifies a draft.
- Errors in document parsing fall back to "needs human review", never
  "best guess."

## 7. No bypassing licensed practice

LFA does not:

- File documents on behalf of a user.
- Authenticate or sign documents.
- Send communications to courts or counterparties on a user's behalf.
- Provide opinions on whether to sue, drop, settle, or appeal.

LFA produces drafts and analyses only. Any action with legal effect
must be taken by the user (with their counsel) or by a licensed
attorney / 법무사.

## 8. No adversarial framing toward the bar

LFA's marketing, documentation, and module descriptions must not
position the system as a replacement for, competitor of, or critique
of licensed legal practice. The framing is collaborative: LFA is
useful to attorneys, paralegals, scriveners, and self-represented
parties simultaneously.

Phrases like "변호사 없이도 가능", "변호사 대비 X% 빠름", "AI 변호사",
or any equivalent are explicitly prohibited in repository content.
