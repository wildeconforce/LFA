"""Module 11 — MULTI_AGENT_ARENA.

Round-based multi-agent courtroom simulation.

Round structure (civil track):
    R1: Plaintiff submits 소장          (CounselPersona[plaintiff])
    R2: Defendant submits 답변서        (CounselPersona[defendant])
    R3: Plaintiff submits 준비서면 1    (LOGIC_BREAKER assist)
    R4: Defendant submits 준비서면 1    (LOGIC_BREAKER assist)
    R5: Plaintiff 준비서면 2
    R6: Defendant 준비서면 2
    ...
    until round limit OR judge signals 변론종결

Criminal track (parallel when civil_and_criminal):
    Prosecutor 공소장 → Defense 변론 → Counter-attack rounds

Each agent's behavior is parameterized by its persona's style
variables (aggression / emotional_appeal / detail_orientation).

Implementation backend: AutoGen or LangGraph (configurable).

This is a SYNTHETIC simulation. Outputs are not legal advice and have
no jurisdictional effect.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from lfa.models.persona import CounselPersona
from lfa.simulation.case_generator import SyntheticCase


class RoundOutput(BaseModel):
    round_number: int
    track: Literal["civil", "criminal"]
    actor_role: str            # plaintiff / defendant / prosecutor / defense
    document_kind: str         # 소장 / 답변서 / 준비서면 / 공소장 / 변론서
    body_text: str
    annotations: list[str] = Field(default_factory=list)


class ArenaTranscript(BaseModel):
    case: SyntheticCase
    rounds: list[RoundOutput]
    closed: bool = False
    closing_reason: str | None = None


def run_arena(
    case: SyntheticCase,
    plaintiff_counsel: CounselPersona,
    defendant_counsel: CounselPersona,
    prosecutor: CounselPersona | None = None,
    defense: CounselPersona | None = None,
    max_rounds: int = 12,
    backend: Literal["autogen", "langgraph", "manual"] = "manual",
) -> ArenaTranscript:
    """Run the round-based mock trial.

    Returns:
        A full transcript of every round in order.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("MULTI_AGENT_ARENA not yet implemented (skeleton)")
