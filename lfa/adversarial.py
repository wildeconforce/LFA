"""Module 14 — ADVERSARIAL_LOOP.

Closed-loop self-correction + counter-strike module.

This module sits at the end of the analysis pipeline and runs three
operations in sequence:

    1. SELF_AUDIT
        Audit our own draft for errors:
            - Factual mistakes
            - Logical gaps
            - Tone problems
            - Citations that fail FACT_VERIFIER
            - Statements that contradict our own prior briefs
        Output: list of `SelfAuditFinding`.

    2. SELF_CORRECT
        Apply fixes to the draft based on `SelfAuditFinding`s.
        Output: revised draft (same kind, same structure).

    3. COUNTER_STRIKE
        Re-run weakness detection against the OPPOSING side's most
        recent brief, but now from the corrected position. This often
        surfaces stronger attacks than the initial LOGIC_BREAKER pass
        because:
            (a) Our position is now internally consistent.
            (b) Errors we found in our own draft hint at parallel
                errors in the opposing draft (mirror-error principle).
            (c) The verified facts from FACT_VERIFIER can now be
                wielded offensively.
        Output: list of `CounterStrikeAttack` with priority ranking.

The loop can iterate (configurable max_iterations). Each iteration
should reduce the count of `SelfAuditFinding`s; when it stops
reducing, the loop terminates.

DESIGN PRINCIPLES:

    - We attack only AFTER we are clean. A draft with internal errors
      cannot credibly attack opposing errors — the opposing side will
      counter-counter with our own mistakes. Self-correct first.

    - Mirror-error principle: an error type we made (e.g. partial
      quotation) is often present in the opposing brief too. SELF_AUDIT
      findings inform COUNTER_STRIKE search.

    - The output is a STRATEGIC RECOMMENDATION SET. The user (with
      counsel) decides which counter-strikes to actually deploy in
      the final brief — defaults from `simulator.AttackVector.should_preempt`
      apply here too: do not volunteer attacks the opposing party has
      not provoked.

This module produces strategic suggestions only. It does not provide
legal advice.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from lfa.models.case import CaseRecord
from lfa.writer import DraftDocument
from lfa.simulator import AttackVector


SelfAuditCategory = Literal[
    "factual_error",
    "logical_gap",
    "tone_problem",
    "unverified_citation",
    "internal_contradiction",
    "weak_phrasing",        # Statement that weakens our position unnecessarily
    "premature_concession", # Conceded a point we did not need to concede
]


class SelfAuditFinding(BaseModel):
    category: SelfAuditCategory
    location_excerpt: str  # the offending excerpt from our draft
    issue: str
    suggested_fix: str
    severity: Literal["block", "must_fix", "nice_to_have"]


class CounterStrikeAttack(BaseModel):
    """An attack against the opposing side, computed from a CLEAN position."""

    target_excerpt: str            # the excerpt from opposing brief being attacked
    attack: str                    # the rebuttal text
    grounding: list[str]           # which verified facts support this attack
    priority: Literal["killshot", "high", "medium", "low"]
    mirror_of: str | None = None   # was this discovered via mirror-error from our SELF_AUDIT?


class AdversarialReport(BaseModel):
    iterations_run: int
    initial_findings_count: int
    final_findings_count: int
    audit_history: list[list[SelfAuditFinding]] = Field(default_factory=list)
    final_draft: DraftDocument
    counter_strikes: list[CounterStrikeAttack]
    converged: bool
    notes: list[str] = Field(default_factory=list)


def run_loop(
    draft: DraftDocument,
    case: CaseRecord,
    opposing_brief_text: str,
    max_iterations: int = 3,
) -> AdversarialReport:
    """Run the adversarial loop on `draft`.

    Args:
        draft: Current draft (typically from `DOC_WRITER`).
        case: Structured case record (for grounding).
        opposing_brief_text: The most recent brief from the opposing
            party. Used for COUNTER_STRIKE.
        max_iterations: Maximum SELF_AUDIT → SELF_CORRECT cycles.

    Returns:
        An `AdversarialReport` containing the final draft, the audit
        history across iterations, and the counter-strike set.

    Note:
        Skeleton implementation — TODO. The implementation calls into
        `self_audit`, `self_correct`, and `counter_strike` below.
    """
    raise NotImplementedError("ADVERSARIAL_LOOP.run_loop not yet implemented (skeleton)")


def self_audit(draft: DraftDocument, case: CaseRecord) -> list[SelfAuditFinding]:
    """Audit our own draft for errors.

    Note:
        Skeleton implementation — TODO. Production version uses an LLM
        with a structured audit prompt that returns category-tagged
        findings.
    """
    raise NotImplementedError("self_audit not yet implemented (skeleton)")


def self_correct(draft: DraftDocument, findings: list[SelfAuditFinding]) -> DraftDocument:
    """Apply fixes to `draft` for each finding.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("self_correct not yet implemented (skeleton)")


def counter_strike(
    revised_draft: DraftDocument,
    opposing_brief_text: str,
    case: CaseRecord,
    audit_findings: list[SelfAuditFinding],
) -> list[CounterStrikeAttack]:
    """Find attacks against the opposing brief from a CLEAN position.

    Args:
        revised_draft: Our draft AFTER self-correction.
        opposing_brief_text: The opposing brief.
        case: Structured case record.
        audit_findings: Our own SELF_AUDIT findings — used to apply
            the mirror-error principle (an error we made is likely
            present on the other side too).

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("counter_strike not yet implemented (skeleton)")
