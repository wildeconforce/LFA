"""Module 5 — HUMAN_REVIEW.

Capture user feedback on AI drafts and apply corrections in a loop.

Feedback categories (`FeedbackKind`):
    - `fact_error`              — factual inaccuracy
    - `frame_risk`              — phrasing weakens the user's position
    - `unnecessary_disclosure`  — exposes a weakness the opposing side
                                  has not raised
    - `tone_issue`              — sounds AI-generated, not credible for
                                  pro se voice
    - `legal_term_risk`         — words like "책임", "인정", "잘못"
                                  carry implicit weight in court
    - `contradiction`           — conflicts with a prior brief by the
                                  same party

Loop: AI draft → user flags → category-routed correction → re-confirm
→ repeat or finalize.

This module preserves the strategic principle that the human (user
or counsel) remains the decision-maker on what to disclose, when, and
how. The AI never decides to expose strategic weaknesses unprompted.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from lfa.writer import DraftDocument


FeedbackKind = Literal[
    "fact_error",
    "frame_risk",
    "unnecessary_disclosure",
    "tone_issue",
    "legal_term_risk",
    "contradiction",
]


class FeedbackItem(BaseModel):
    kind: FeedbackKind
    target_excerpt: str  # the exact text the user is flagging
    user_note: str       # what the user wants changed
    severity: Literal["block", "must_fix", "nice_to_have"]


class ReviewSession(BaseModel):
    draft: DraftDocument
    feedback: list[FeedbackItem]
    iteration: int = 0
    finalized: bool = False


def collect_feedback(draft: DraftDocument) -> list[FeedbackItem]:
    """Interactive prompt to collect user feedback on a draft.

    Note:
        Skeleton implementation — TODO. CLI variant: rich-based prompts.
        API variant: returns from caller-provided feedback payload.
    """
    raise NotImplementedError("collect_feedback not yet implemented (skeleton)")


def apply_feedback(session: ReviewSession) -> DraftDocument:
    """Apply collected feedback to produce a revised draft.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("apply_feedback not yet implemented (skeleton)")
