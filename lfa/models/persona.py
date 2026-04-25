"""Persona models for the Mock Trial Engine.

Personas are loaded from NVIDIA Nemotron-Personas-Korea (synthetic
Korean personas grounded in KOSIS + Supreme Court statistics, with
PII-zero / PIPA-compliant guarantees).

Judge and counsel personas extend the base persona with
profession-specific behavioral variables that drive multi-agent
courtroom simulation.

All personas are SYNTHETIC. Any resemblance to real persons is
coincidental.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Gender = Literal["male", "female", "unspecified"]


class Persona(BaseModel):
    """Base synthetic Korean persona."""

    persona_id: str  # opaque ID from Nemotron-Personas-Korea
    name: str        # synthetic; not a real person
    age: int
    gender: Gender
    occupation: str
    region: str      # 서울 / 경기 / 부산 / ...
    family_structure: str | None = None  # e.g. "기혼·자녀 2명"
    financial_state: str | None = None   # e.g. "월수입 ~300만원"
    background_notes: str | None = None  # qualitative free text


class JudgePersona(Persona):
    """A synthetic judge with behavioral parameters that drive rulings.

    The four axes are derived from observable patterns in Korean
    judicial practice and are intentionally configurable so that the
    simulator can produce a distribution of outcomes for the same
    case across different judicial temperaments.
    """

    rigor: float = Field(0.5, ge=0, le=1)
    """0 = skims the file, 1 = exhaustively reads every page."""

    pace: float = Field(0.5, ge=0, le=1)
    """0 = decides quickly, 1 = takes long under careful deliberation."""

    rationality: float = Field(0.5, ge=0, le=1)
    """0 = sympathy-driven, 1 = strict legal-doctrine-driven."""

    precedent_dependence: float = Field(0.5, ge=0, le=1)
    """0 = trusts intuition, 1 = heavily relies on cited precedent."""


class CounselPersona(Persona):
    """A synthetic counsel (변호사 or 검사) with style parameters."""

    side: Literal["plaintiff", "defendant", "prosecution", "defense"]

    aggression: float = Field(0.5, ge=0, le=1)
    """0 = defensive, 1 = highly offensive in tone."""

    emotional_appeal: float = Field(0.5, ge=0, le=1)
    """0 = pure law-and-fact, 1 = strong emotional/sympathetic framing."""

    detail_orientation: float = Field(0.5, ge=0, le=1)
    """0 = broad strokes, 1 = obsessive procedural detail."""
