"""Module 8 — TIMELINE_CONFLICT_DETECTOR.

Detect chronological contradictions across statements, evidence, and
prior decisions.

Use cases:
    - One party claims event A occurred before event B, but evidence
      shows the reverse.
    - A 녹취 timestamp implies a state of affairs that contradicts a
      later 준비서면 statement.
    - A prior judgment establishes a fact that the current brief
      contradicts.

Outputs both a list of conflicts and a "favorable arrangement" — the
user-favorable framing of the same set of events that is also fully
consistent with the source materials.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from lfa.models.case import CaseRecord, TimelineEvent


class TimelineConflict(BaseModel):
    event_a: TimelineEvent
    event_b: TimelineEvent
    contradiction_type: Literal[
        "ordering",         # claimed before/after disagrees with evidence
        "duration",         # claimed gap differs from evidence
        "simultaneity",     # claimed simultaneous, evidence shows offset
        "existence",        # one source says it happened, another denies
    ]
    severity: Literal["critical", "material", "minor"]
    description: str


class TimelineReport(BaseModel):
    conflicts: list[TimelineConflict]
    favorable_arrangement: list[TimelineEvent]  # consistent + favorable
    notes: list[str] = []


def detect_conflicts(case: CaseRecord) -> TimelineReport:
    """Detect timeline conflicts in the case record.

    Returns:
        A `TimelineReport` with conflicts and a favorable arrangement
        of consistent events.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("TIMELINE_CONFLICT_DETECTOR not yet implemented (skeleton)")
