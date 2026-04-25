# LFA — Legal Framework Analysis

> Modular framework for analyzing Korean civil and criminal cases.
> Built for legal professionals and self-represented litigants alike,
> as an assistive analysis tool — not a substitute for licensed legal advice.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: Active Development](https://img.shields.io/badge/status-active--development-orange.svg)]()

---

## What is LFA

LFA is a 14-module open-source framework for analyzing legal cases that
mix civil monetary claims (`약정금`, `대여금`) with criminal overlays
(`공갈`, `협박`, `갈취`, `사기`).

The system breaks legal analysis into composable stages:

```
[Case Input]
    ↓
CASE_SCANNER → LOGIC_BREAKER → PRECEDENT_HUNTER → DOC_WRITER
                                                       ↓
                                                [Draft Output]
                                                       ↓
                                                HUMAN_REVIEW
                                                       ↓
                                                FACT_VERIFIER
                                                       ↓
                                                [Final Output]
```

Plus a Mock Trial Simulator that uses synthetic Korean personas to
run multi-agent courtroom simulations end-to-end.

## Why LFA exists

Korea has one of the highest rates of self-represented litigation in
the developed world. Civil and criminal proceedings frequently
intersect in cases involving compelled financial agreements
(`강박에 의한 의사표시`), and the analytical work — fact organization,
weakness detection, precedent verification, document drafting,
internal consistency checking — is repetitive but high-stakes.

LFA modularizes that analytical work so it can be done systematically,
auditably, and reproducibly. The framework is designed to *assist*
licensed practitioners (attorneys, paralegals, judicial scriveners)
and to *support* self-represented parties working alongside their
counsel — never to replace either.

## Two complementary tracks

### 📊 Analysis track (Modules 1–8)

Static analysis of an existing case file.

| Module | Purpose |
|--------|---------|
| 1. CASE_SCANNER | Parse 소장·판결문·녹취록·준비서면 → structured facts |
| 2. LOGIC_BREAKER | Detect logical/temporal/evidentiary weaknesses |
| 3. PRECEDENT_HUNTER | Search and **cross-verify** Supreme Court precedents |
| 4. DOC_WRITER | Generate brief/answer/demand-letter drafts |
| 5. HUMAN_REVIEW | Capture user feedback and apply corrections |
| 6. FACT_VERIFIER | Cross-check facts against source documents |
| 7. COUNTER_SIMULATOR | Red-team the draft from opposing counsel's perspective |
| 8. TIMELINE_CONFLICT_DETECTOR | Detect chronological contradictions |
| 14. ADVERSARIAL_LOOP | Self-audit → self-correct → counter-strike (closes the analysis loop) |

### 🎭 Simulation track (Modules 9–13) — Mock Trial Engine

Synthetic case generation and multi-agent courtroom simulation.

| Module | Purpose |
|--------|---------|
| 9. PERSONA_LOADER | Load synthetic Korean personas (Nemotron-Personas-Korea) |
| 10. CASE_GENERATOR | Generate fictional cases with asymmetric evidence |
| 11. MULTI_AGENT_ARENA | Round-based mock trial (plaintiff/defendant/prosecutor/defense) |
| 12. JUDGE_ADJUDICATOR | Persona-driven judge rulings (1심/2심) |
| 13. OUTCOME_ANALYZER | Aggregate outcomes across judge/strategy matrices |

## Synthetic case-driven development

LFA modules are designed and validated against **fully synthetic Korean
legal cases** — no real-world cases or PII are used in this repository.

Synthetic data sources:

1. **NVIDIA Nemotron-Personas-Korea** — 6M synthetic Korean personas
   grounded in KOSIS statistics + Supreme Court case data, with
   PII-zero / PIPA-compliant guarantees. Used for parties, judges,
   counsel, and witnesses.
2. **Public precedent patterns** — Anonymized rulings from
   `law.go.kr` and the Supreme Court Comprehensive Legal Information
   System, generalized into pattern templates.
3. **LLM synthesis** — Direct generation of fictional Korean
   civil/criminal scenarios via Claude / GPT prompts.

All identifying details (names, case numbers, dates, addresses,
amounts) in fixtures and examples are fictional. Any resemblance to
real persons or cases is coincidental.

See [`docs/SYNTHETIC_DATA.md`](docs/SYNTHETIC_DATA.md) for the full
generation methodology.

## Hallucination prevention

Korean precedent hallucination is a fatal flaw in any legal AI tool.
LFA enforces a strict verification rule:

> Every cited precedent must be confirmed by **at least 2 of the
> following 4 sources** before it appears in any output:
>
> 1. 국가법령정보센터 (`law.go.kr`)
> 2. CaseNote (`casenote.kr`)
> 3. BigCase (`bigcase.ai`)
> 4. 대법원 종합법률정보 (`glaw.scourt.go.kr`)

Citations that fail verification are deleted, not generated. Target
fabrication rate: 0%.

See [`docs/SAFETY.md`](docs/SAFETY.md) for the full safety contract.

## Positioning — assistive, not adversarial

LFA's relationship to the Korean legal profession is explicitly
collaborative:

- **DO** use LFA to organize facts, surface weaknesses, draft
  outlines, and red-team strategies.
- **DO NOT** treat LFA output as legal advice. Every output ends with
  a disclaimer: *"본 내용은 법률적 조언이 아닌 전략적 참고 자료입니다.
  실제 소송 행위 시에는 반드시 변호사 또는 법무사의 검토를 거치시기
  바랍니다."*
- LFA is built to be useful to licensed counsel (efficiency),
  paralegals/scriveners (workflow), and self-represented parties
  (decision support) simultaneously. It does not position itself
  against any of these groups.

## Status

🚧 **Active development.** This is `v0` — module interfaces and
project skeleton. Working implementations land module-by-module.

| Phase | Scope | Status |
|-------|-------|--------|
| v0 | Skeleton + interfaces | 🟢 Current |
| v0.1 | CASE_SCANNER + LOGIC_BREAKER + DOC_WRITER (analysis core) | ⏳ Next |
| v0.2 | PRECEDENT_HUNTER + FACT_VERIFIER + safety rails | ⏳ |
| v0.3 | Synthetic case fixtures + tests | ⏳ |
| v0.4 | Mock Trial Engine (Modules 9–13) | ⏳ |
| v1.0 | First stable release | ⏳ |

## Quickstart

```bash
git clone https://github.com/wildeconforce/LFA.git
cd LFA
pip install -e ".[dev]"

# (skeleton only — not functional yet)
python -m lfa --help
```

## Project layout

```
lfa/
├── README.md                       (this file)
├── LICENSE                         (MIT)
├── pyproject.toml
├── lfa/
│   ├── scanner.py                  Module 1: CASE_SCANNER
│   ├── breaker.py                  Module 2: LOGIC_BREAKER
│   ├── hunter.py                   Module 3: PRECEDENT_HUNTER
│   ├── writer.py                   Module 4: DOC_WRITER
│   ├── reviewer.py                 Module 5: HUMAN_REVIEW
│   ├── verifier.py                 Module 6: FACT_VERIFIER
│   ├── simulator.py                Module 7: COUNTER_SIMULATOR
│   ├── timeline.py                 Module 8: TIMELINE_CONFLICT_DETECTOR
│   ├── adversarial.py              Module 14: ADVERSARIAL_LOOP
│   ├── simulation/
│   │   ├── persona_loader.py       Module 9
│   │   ├── case_generator.py       Module 10
│   │   ├── arena.py                Module 11
│   │   ├── judge_adjudicator.py    Module 12
│   │   └── outcome_analyzer.py     Module 13
│   ├── api/                        Source-system clients
│   ├── models/                     Pydantic data models
│   ├── templates/                  Document templates
│   └── utils/                      PDF parsing, OCR, redaction, dates
├── data/
│   ├── synthetic/                  Generated synthetic cases
│   └── precedents/                 Verified precedent cache
├── examples/
│   └── synthetic_case_demo.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── MODULES.md
│   ├── SAFETY.md
│   └── SYNTHETIC_DATA.md
└── tests/
    └── fixtures/
```

## Acknowledgements

LFA's Mock Trial Engine (Track B) builds on **NVIDIA Nemotron-Personas-Korea**,
a synthetic Korean persona dataset that made the simulation track viable.
Without it, generating realistic-distribution synthetic cases that respect
PII/PIPA constraints would not have been practical for an open-source
project.

> **NVIDIA Nemotron-Personas-Korea** — 6M synthetic Korean personas
> grounded in KOSIS statistics + Supreme Court case data. PII-zero,
> PIPA-compliant.
>
> https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea

We use the dataset under its published license terms. See
[`docs/SYNTHETIC_DATA.md`](docs/SYNTHETIC_DATA.md) for how the dataset
flows through Module 9 (`PERSONA_LOADER`) into the rest of the
simulation pipeline.

Additional public sources used for pattern templates:
- 국가법령정보센터 (`law.go.kr`)
- 대법원 종합법률정보 (`glaw.scourt.go.kr`)
- CaseNote (`casenote.kr`)
- BigCase (`bigcase.ai`)

## License

MIT — see [`LICENSE`](LICENSE).

The synthetic-persona data shipped with LFA fixtures is generated from
NVIDIA Nemotron-Personas-Korea under that dataset's own license. See
[`docs/SYNTHETIC_DATA.md`](docs/SYNTHETIC_DATA.md).

## Disclaimer

**This software does not provide legal advice.** All outputs are
strategic reference materials only. Any party intending to act on
LFA output must obtain review from a licensed attorney or judicial
scrivener (`법무사`) authorized to practice in the relevant
jurisdiction.

The maintainers and contributors of LFA disclaim all liability for
outcomes arising from the use of this software.

---

본 시스템은 법률적 조언을 제공하지 않습니다. 모든 출력물은 전략적
참고 자료이며, 실제 소송 행위 시에는 반드시 변호사 또는 법무사의
검토를 거치시기 바랍니다.
