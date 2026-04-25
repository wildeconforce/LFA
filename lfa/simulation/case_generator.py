"""Module 10 — CASE_GENERATOR.

Generate fictional Korean civil/criminal cases for simulation.

Inputs:
    - Issue keyword set (e.g. ["약정금", "공갈", "협박"])
    - Loaded personas (parties + judges + counsel)
    - Asymmetry parameter — how strongly to slant evidence in favor
      of one party at the start of the simulation. The simulator's
      job is to discover whether that initial advantage holds up
      under the opposing side's pressure.

Outputs:
    A `SyntheticCase` with:
        - Time-ordered fictional events
        - Asymmetrically distributed evidence (e.g. 60/40 plaintiff)
        - Fictional 진술 / 녹취 / 문자 / 카톡 / 계좌이체 records
        - Initial party claims

All identifying details are fictional. Any resemblance to real cases
is coincidental.

This module is the foundation of "synthetic case-driven development":
modules are designed and tested against generated cases before being
applied to any real-world input.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from lfa.models.case import CaseRecord
from lfa.models.persona import Persona


CaseTrack = Literal["civil_only", "criminal_only", "civil_and_criminal"]


class CaseGenerationConfig(BaseModel):
    issue_keywords: list[str]
    track: CaseTrack = "civil_and_criminal"
    asymmetry_bias: float = Field(0.5, ge=0, le=1)
    """0 = balanced; 1 = strongly favored toward plaintiff;
    interpolate accordingly."""
    plaintiff_persona: Persona
    defendant_persona: Persona
    seed: int = 42


class SyntheticCase(CaseRecord):
    """A fictional case generated for simulation. Inherits CaseRecord."""

    generation_config: dict
    is_synthetic: bool = True


def generate_case(config: CaseGenerationConfig) -> SyntheticCase:
    """Generate a fictional case according to `config`.

    Returns:
        A `SyntheticCase` ready to be loaded into the arena.

    Note:
        Skeleton implementation — TODO. Production version uses an
        LLM (Claude/GPT) with carefully designed prompts to produce
        coherent fictional cases that mirror typical Korean civil/
        criminal patterns without resembling any specific real case.
    """
    raise NotImplementedError("CASE_GENERATOR not yet implemented (skeleton)")
