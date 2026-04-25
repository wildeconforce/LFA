"""Source-system API clients used by PRECEDENT_HUNTER (Module 3).

    - law_api.py      — 국가법령정보센터 (law.go.kr)
    - casenote_api.py — CaseNote (casenote.kr)
    - bigcase_api.py  — BigCase (bigcase.ai)
    - glaw_api.py     — 대법원 종합법률정보 (glaw.scourt.go.kr)

Each client implements a `verify(case_number) -> bool` interface and
is consumed by `lfa.hunter.verify_precedent()` for the 2-of-4
verification rule.
"""
