"""Module 6 — FACT_VERIFIER.

Cross-check every AI-generated claim against source documents.

Verification targets (six categories):
    1. Dates           — every date mentioned must match the original
                         source document where it first appears.
    2. Quoted speech   — verbatim quotes from 녹취록 / 판결문 must
                         match source text character-for-character
                         (whitespace and punctuation tolerant).
    3. Case numbers    — every cited 판례 number must pass
                         `hunter.verify_precedent()` cross-check.
    4. Case progression — claims about prior decisions must not
                         conflict with the actual judgment text.
    5. Evidence numbers — references like 갑제3호증 / 을제5호증 must
                         match the evidence list of the case file.
    6. Party statements — internal consistency across briefs by the
                         same party.

Output: a verification report with a `safe_to_submit` flag. If any
critical conflict is found, `safe_to_submit` is False and a human
must intervene.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from lfa.models.case import CaseRecord
from lfa.writer import DraftDocument


VerificationCategory = Literal[
    "date",
    "quoted_speech",
    "case_number",
    "case_progression",
    "evidence_number",
    "party_statement",
]


class Conflict(BaseModel):
    category: VerificationCategory
    excerpt: str  # the AI-generated text that fails verification
    expected: str | None  # what the source actually says (if known)
    severity: Literal["critical", "warning", "info"]


class VerificationReport(BaseModel):
    conflicts: list[Conflict]
    safe_to_submit: bool
    action_required: str  # human-readable next-step instruction


def verify_draft(draft: DraftDocument, case: CaseRecord) -> VerificationReport:
    """Verify all factual claims in `draft` against `case` source data.

    Returns:
        A `VerificationReport`. `safe_to_submit` is True iff no
        critical conflicts are found.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("FACT_VERIFIER not yet implemented (skeleton)")
