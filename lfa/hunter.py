"""Module 3 — PRECEDENT_HUNTER.

Search Korean Supreme Court precedents and statutes by issue keyword,
then **cross-verify** existence before citation.

VERIFICATION RULE — non-negotiable:

    Every cited precedent must be confirmed by at least 2 of the
    following 4 sources before it appears in any output:

        1. 국가법령정보센터 (law.go.kr)
        2. CaseNote (casenote.kr)
        3. BigCase (bigcase.ai)
        4. 대법원 종합법률정보 (glaw.scourt.go.kr)

    Citations that fail verification are deleted, not generated.
    Target hallucination rate: 0%.

This rule is enforced inside `verify_precedent`. Any caller that
bypasses verification is in violation of LFA's safety contract.

See `docs/SAFETY.md` for the full policy.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


VerificationSource = Literal["law_go_kr", "casenote", "bigcase", "glaw_scourt"]


class PrecedentCitation(BaseModel):
    case_number: str  # e.g. "97다24276"
    court: str  # e.g. "대법원"
    decision_date: str  # ISO yyyy-mm-dd
    summary: str
    relevance: str
    verified: bool
    verification_sources: list[VerificationSource]


class StatuteCitation(BaseModel):
    law_name: str
    article: str
    text: str
    verified: bool


class HunterReport(BaseModel):
    precedents: list[PrecedentCitation]
    statutes: list[StatuteCitation]


def hunt_precedents(issue_keywords: list[str], min_count: int = 3) -> HunterReport:
    """Search precedents and statutes for the given legal issues.

    Args:
        issue_keywords: e.g. ["강박에 의한 의사표시", "공갈죄"]
        min_count: Minimum number of verified precedents to return per
            issue. Stricter = more reliable.

    Returns:
        A `HunterReport` with only cross-verified citations.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("PRECEDENT_HUNTER not yet implemented (skeleton)")


def verify_precedent(case_number: str) -> tuple[bool, list[VerificationSource]]:
    """Verify a precedent's existence across the 4 source databases.

    Returns:
        (verified, sources_confirming) where `verified` is True iff at
        least 2 sources confirm the citation.

    Note:
        Skeleton implementation — TODO. This function is the gate
        that prevents hallucinated case numbers from reaching outputs.
    """
    raise NotImplementedError("verify_precedent not yet implemented (skeleton)")
