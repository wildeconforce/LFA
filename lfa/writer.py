"""Module 4 — DOC_WRITER.

Generate draft legal documents from structured case data.

Document kinds supported:
    - 준비서면 (preparatory brief)
    - 답변서 (answer)
    - 내용증명 (content-certified mail)
    - 탄원서 (petition)
    - 고소장 (criminal complaint draft)

Tone-and-manner profiles:
    - `professional`  — attorney register, dense statute citations
    - `human`         — pro se register, narrative voice, sincerity
    - `hybrid`        — narrative scaffolding with statute citations

MANDATORY footer (auto-appended, cannot be disabled):

    "본 내용은 법률적 조언이 아닌 전략적 참고 자료입니다.
     실제 소송 행위 시에는 반드시 변호사 또는 법무사의 검토를
     거치시기 바랍니다."

Outputs are ALWAYS drafts. They MUST be reviewed by licensed counsel
or a 법무사 before submission to any court or counterparty.
"""

from __future__ import annotations

from typing import Literal
from pathlib import Path

from pydantic import BaseModel

from lfa.models.case import CaseRecord
from lfa.breaker import BreakerReport
from lfa.hunter import HunterReport


DocumentKind = Literal[
    "preparatory_brief",  # 준비서면
    "answer",             # 답변서
    "content_certified",  # 내용증명
    "petition",           # 탄원서
    "criminal_complaint", # 고소장
]

ToneProfile = Literal["professional", "human", "hybrid"]


class DraftDocument(BaseModel):
    kind: DocumentKind
    tone: ToneProfile
    body_text: str  # plain text body (Markdown-ish)
    output_path: Path | None = None  # set when materialized to disk
    disclaimer: str  # always populated; never empty


def write_document(
    case: CaseRecord,
    kind: DocumentKind = "preparatory_brief",
    tone: ToneProfile = "hybrid",
    breaker: BreakerReport | None = None,
    hunter: HunterReport | None = None,
    output_path: str | Path | None = None,
) -> DraftDocument:
    """Generate a draft document.

    Args:
        case: Structured case record.
        kind: Document type.
        tone: Tone-and-manner profile.
        breaker: Optional weakness analysis to weave into argumentation.
        hunter: Optional verified precedent set to cite.
        output_path: If provided, write a DOCX file to this path.

    Returns:
        A `DraftDocument` with body text and disclaimer footer.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("DOC_WRITER not yet implemented (skeleton)")
