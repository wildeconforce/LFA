"""Pydantic models for structured case data."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


PartyRole = Literal[
    "plaintiff",       # 원고
    "defendant",       # 피고
    "appellant",       # 항소인
    "respondent",      # 피항소인
    "complainant",     # 고소인
    "accused",         # 피고소인 / 피의자 / 피고인
]

ActorSide = Literal["plaintiff", "defendant", "court", "third_party"]

CaseType = Literal[
    "약정금",
    "대여금",
    "손해배상",
    "공갈",
    "협박",
    "사기",
    "기타",
]


class Party(BaseModel):
    """A natural person or entity involved in the case."""

    name: str
    role: PartyRole
    address: str | None = None  # may be redacted
    contact: str | None = None  # may be redacted


class TimelineEvent(BaseModel):
    """A single fact-bearing event placed on the case timeline."""

    occurred_on: date
    description: str
    actor: ActorSide
    evidence_refs: list[str] = Field(default_factory=list)
    source_document: str | None = None  # which case-file doc described it


class EvidenceItem(BaseModel):
    """A single piece of evidence (갑/을 호증 or court-record item)."""

    label: str  # e.g. "갑제3호증", "을제5호증"
    title: str
    submitted_by: ActorSide
    submission_date: date | None = None
    summary: str | None = None
    file_refs: list[str] = Field(default_factory=list)


class PriorDecision(BaseModel):
    """A prior judicial / prosecutorial decision related to the case."""

    case_number: str
    court: str
    kind: Literal["civil", "criminal", "prosecution", "police", "other"]
    decision_date: date
    result: str  # 유죄 / 무죄 / 기각 / 불기소 / 불송치 / 인용 / 일부인용
    summary: str | None = None


class CaseRecord(BaseModel):
    """The full structured representation of a case file.

    This is the central data model. Every analysis module consumes a
    `CaseRecord`; every parsing module produces one.
    """

    case_id: str  # e.g. "XXXX나XXXXX 약정금"
    case_type: CaseType
    parties: list[Party]
    claim_amount_krw: int | None = None
    timeline: list[TimelineEvent] = Field(default_factory=list)
    plaintiff_claims: list[str] = Field(default_factory=list)
    defendant_claims: list[str] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    prior_decisions: list[PriorDecision] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    # Provenance
    source_files: list[str] = Field(default_factory=list)
    extracted_at: date | None = None
