# Synthetic data methodology

LFA modules are designed and validated against fully synthetic
Korean legal cases. This document describes the three generation
sources LFA uses and the rules that govern all fixture data.

## Why synthetic-only

1. **Privacy.** Real Korean legal cases involve identifiable
   parties, addresses, financial details, and minors. Even
   "anonymized" real cases retain identifying patterns when combined
   with the case-number registry. Synthetic-only avoids this entirely.
2. **Reproducibility.** A synthetic case keyed on a seed and
   configuration produces the same result on every machine. Real
   cases have arbitrary one-off content that cannot be regenerated.
3. **Coverage.** Synthetic generation can produce edge cases (rare
   evidence configurations, unusual procedural histories) that real
   data may not contain.
4. **Safety.** Open-sourcing fixtures requires that no fixture
   resemble a specific real case. Synthetic fixtures clear that bar
   by construction.

## Three generation sources

### Source 1 — NVIDIA Nemotron-Personas-Korea

> https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea

Used for: parties, judges, counsel, prosecutors, witnesses.

**Properties:**
- 6M synthetic Korean personas.
- Grounded in KOSIS (통계청) statistics + Supreme Court case data.
- PII-zero by construction.
- PIPA (개인정보 보호법) compliant.
- Demographic distribution matches Korean society
  (age × region × occupation × family × financial state).

**LFA usage (Module 9 — `PERSONA_LOADER`):**
1. One-time index build via `build_index(dataset_path, db_path)`.
2. Filtered sampling via `load_personas(role, count, constraints, seed)`.
3. For judge / counsel roles, behavioral axes (rigor / pace /
   rationality / precedent_dependence and aggression /
   emotional_appeal / detail_orientation) are sampled or specified
   on top of the base persona.

### Source 2 — Public precedent pattern extraction

Used for: case templates, typical procedural sequences, recurring
claim/defense structures.

**Properties:**
- Source: public Korean precedent databases (`law.go.kr` and the
  Supreme Court Comprehensive Legal Information System
  `glaw.scourt.go.kr`).
- Patterns are extracted from already-anonymized published rulings.
- Patterns are then **generalized** by an LLM into templates that
  preserve structure while removing all factual specifics.
- The output template never references the source ruling.

**LFA usage (Module 10 — `CASE_GENERATOR`):**
1. Curate a pattern library per issue keyword (`약정금`, `대여금`,
   `공갈`, `협박`, `사기`, etc.).
2. Generation samples a template, then fills it with persona-driven
   fictional content.

### Source 3 — Direct LLM synthesis

Used for: free-form fictional case scenarios, edge-case construction,
dialogue (녹취 / 카톡) generation.

**Properties:**
- An LLM (Claude / GPT) is prompted with a structured spec
  (parties, time range, issue keywords, asymmetry bias).
- Output is fictional content that is consistent with Korean civil
  / criminal procedure but does not reference any specific real
  case.
- Outputs are checked for resemblance to public real cases via a
  similarity gate before being added to fixtures.

**LFA usage (Module 10 — `CASE_GENERATOR`):**
1. Combine with Source 1 personas and Source 2 templates.
2. The LLM fills in narrative content (dialogue, statements,
   document text).
3. Final synthetic case is stamped `is_synthetic=true`.

## Fixture rules

Every fixture in `data/synthetic/` and `tests/fixtures/` MUST satisfy
all of:

1. **Synthetic-only origin.** Generated from one or more of the three
   sources above. No real-case material under any conditions.
2. **Stamped `is_synthetic=true`.** Loaders refuse to consume fixtures
   without this stamp.
3. **Disclaimer in metadata.** Every fixture file includes a header
   stating it is fictional.
4. **No resemblance to specific real cases.** Reviewers should be
   able to read a fixture and not identify any real person, real
   case number, or real proceeding.
5. **No real PII even by accident.** Fixtures pass through
   `lfa.utils.redactor.redact()` before commit, even though they are
   already synthetic — defense in depth.

## Reviewer checklist (PR template)

When a contributor adds or modifies a fixture, the reviewer must
verify:

- [ ] All names appear nowhere in news, court records, or social
      media (quick web search).
- [ ] Case number format is plausible but not a real registered
      number (search the case-number registry).
- [ ] Dates do not match any high-profile real case.
- [ ] Amounts are not specific to any reported real case.
- [ ] Geographic details (addresses, courts, regions) are plausible
      but not real-case-tied.
- [ ] `is_synthetic=true` is set.
- [ ] Header disclaimer is present.

If any box fails, the fixture is regenerated, not patched.

## Why this matters

A legal-tech tool that reaches production with even one real-case
detail in its fixtures has a permanent credibility problem and
potential legal exposure. The synthetic-only rule is what lets LFA
be open-source, public, and safe to use simultaneously.
