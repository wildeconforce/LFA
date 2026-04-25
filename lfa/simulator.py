"""Module 7 — COUNTER_SIMULATOR (red team).

Simulate opposing counsel's attack on the user's draft, identifying
attack vectors before the actual hearing.

For each potential attack the simulator emits:
    - target           — which paragraph / claim is being attacked
    - attack           — the rebuttal an opposing counsel might raise
    - risk_level       — high / medium / low
    - should_preempt   — whether the user should address this in the
                         draft preemptively, or leave it dormant

KEY STRATEGIC PRINCIPLE — `should_preempt` defaults to FALSE.

If the opposing party has not raised an issue, the user should not
volunteer it. Disclosing latent weaknesses unprompted can hand the
opposing side ammunition they would have otherwise missed. The
default is silence; the user (with counsel) decides exceptions.

This is the single most important defensive doctrine of LFA.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from lfa.models.case import CaseRecord
from lfa.writer import DraftDocument


class AttackVector(BaseModel):
    target: str
    attack: str
    risk_level: Literal["high", "medium", "low"]
    should_preempt: bool = False  # explicit default — DO NOT volunteer


class SimulatorReport(BaseModel):
    attack_vectors: list[AttackVector]
    overall_risk: Literal["high", "medium", "low"]


def red_team(draft: DraftDocument, case: CaseRecord) -> SimulatorReport:
    """Simulate opposing counsel's attacks on the draft.

    Returns:
        A `SimulatorReport` with attack vectors and recommendations.
        `should_preempt` defaults to False on every vector.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("COUNTER_SIMULATOR not yet implemented (skeleton)")
