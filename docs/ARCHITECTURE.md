# LFA Architecture

LFA is a 14-module framework split into two complementary tracks
plus a closing adversarial loop.

## Track A — Analysis (Modules 1–8)

Static analysis of an existing case file.

```
[Case input: PDF / DOCX / HWP / images / text]
        ↓
┌─────────────────────────────────────────────────┐
│  1. CASE_SCANNER                                 │
│     parse heterogeneous inputs → CaseRecord     │
└─────────────────────────────────────────────────┘
        ↓ CaseRecord
┌─────────────────────────────────────────────────┐
│  2. LOGIC_BREAKER     |  8. TIMELINE_DETECTOR    │
│     weakness-detect   |     chronological        │
│     opposing claims   |     conflict-detect      │
└─────────────────────────────────────────────────┘
        ↓ BreakerReport          ↓ TimelineReport
┌─────────────────────────────────────────────────┐
│  3. PRECEDENT_HUNTER                             │
│     find + verify Supreme Court precedents      │
│     (≥2 of 4 sources required)                  │
└─────────────────────────────────────────────────┘
        ↓ HunterReport
┌─────────────────────────────────────────────────┐
│  4. DOC_WRITER                                   │
│     generate brief / answer / demand draft      │
└─────────────────────────────────────────────────┘
        ↓ DraftDocument
┌─────────────────────────────────────────────────┐
│  5. HUMAN_REVIEW                                 │
│     iterate with user feedback                  │
└─────────────────────────────────────────────────┘
        ↓ revised draft
┌─────────────────────────────────────────────────┐
│  6. FACT_VERIFIER                                │
│     cross-check every claim vs source docs      │
└─────────────────────────────────────────────────┘
        ↓ VerificationReport
┌─────────────────────────────────────────────────┐
│  7. COUNTER_SIMULATOR (red team)                 │
│     simulate opposing counsel attacks           │
└─────────────────────────────────────────────────┘
        ↓ SimulatorReport
┌─────────────────────────────────────────────────┐
│  14. ADVERSARIAL_LOOP                            │
│      SELF_AUDIT → SELF_CORRECT → COUNTER_STRIKE  │
│      (iterate until convergence)                 │
│      attack from a CLEAN position only           │
│      mirror-error principle: our errors hint     │
│      at parallel errors in the opposing brief    │
└─────────────────────────────────────────────────┘
        ↓ AdversarialReport
[Final draft + safe_to_submit flag + counter-strikes]
```

## Track B — Simulation (Modules 9–13)

Synthetic case generation and multi-agent courtroom simulation.

```
[Issue keywords: 약정금, 공갈, 협박, ...]
        ↓
┌─────────────────────────────────────────────────┐
│  9. PERSONA_LOADER                               │
│     sample synthetic personas from Nemotron     │
│     (parties, judges, counsel, prosecutor)       │
└─────────────────────────────────────────────────┘
        ↓ Personas
┌─────────────────────────────────────────────────┐
│  10. CASE_GENERATOR                              │
│      LLM-synthesize fictional case w/ asymmetric│
│      evidence and full doc trail                │
└─────────────────────────────────────────────────┘
        ↓ SyntheticCase (CaseRecord subclass)
┌─────────────────────────────────────────────────┐
│  11. MULTI_AGENT_ARENA                           │
│      round-based mock trial:                    │
│      소장 → 답변서 → 준비서면 → 반박 ...        │
└─────────────────────────────────────────────────┘
        ↓ ArenaTranscript
┌─────────────────────────────────────────────────┐
│  12. JUDGE_ADJUDICATOR                           │
│      persona-driven 판결                        │
│      same case × different judges = different   │
│      outcomes — that's the point                │
└─────────────────────────────────────────────────┘
        ↓ Ruling × N (matrix)
┌─────────────────────────────────────────────────┐
│  13. OUTCOME_ANALYZER                            │
│      aggregate distribution; feedback to        │
│      LOGIC_BREAKER as training signal           │
└─────────────────────────────────────────────────┘
        ↓ training patterns
[Track A modules improve from Track B insights]
```

## Cross-track feedback

Track B's value is not "predicting court outcomes." It is generating
**outcome distributions** that, in aggregate, surface which arguments
work against which judicial temperaments. Those patterns feed back
into Track A's LOGIC_BREAKER to make weakness-detection more accurate.

This is the loop that makes LFA more than a static document generator.

## Data backbone

Every module produces or consumes Pydantic models defined in
`lfa.models`:

- `CaseRecord` — central case representation
- `Persona` / `JudgePersona` / `CounselPersona` — synthetic actors
- `BreakerReport`, `HunterReport`, `DraftDocument`,
  `VerificationReport`, `SimulatorReport`, `TimelineReport`,
  `ArenaTranscript`, `Ruling`, `OutcomeSummary`

Models are versioned via Pydantic; breaking changes require migration
notes in `docs/CHANGELOG.md`.

## What LFA is NOT

- Not a substitute for licensed legal counsel.
- Not a real-court-outcome predictor.
- Not a tool for adversarial use against the legal profession.
- Not a place to store real case materials. Use the `local_cases/`
  folder convention which is gitignored, and only on machines under
  your direct control.
