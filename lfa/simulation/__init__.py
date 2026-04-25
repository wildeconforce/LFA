"""Mock Trial Engine — Modules 9–13.

Multi-agent courtroom simulation using synthetic Korean personas.

Architecture:

    [Nemotron-Personas-Korea (synthetic personas)]
            ↓ extract
        plaintiff / defendant / 1심 judge / 2심 judge / counsel / prosecutor
            ↓
    [CASE_GENERATOR] keyword → fictional case + asymmetric evidence
            ↓
    [MULTI_AGENT_ARENA] round-based mock trial
        R1 소장 → R2 답변서 → R3 준비서면 → R4 반박 ...
        criminal track parallel: 검사 ↔ 피고 변호인
            ↓
    [JUDGE_ADJUDICATOR] persona-driven rulings (1심 + 2심)
            ↓
    [OUTCOME_ANALYZER] outcome distribution across judge×strategy matrix
            ↓
    feedback loop → LOGIC_BREAKER training data

All personas, cases, and outcomes in this engine are synthetic. No
real-world cases or persons are referenced.
"""

from lfa.simulation.persona_loader import load_personas
from lfa.simulation.case_generator import generate_case
from lfa.simulation.arena import run_arena
from lfa.simulation.judge_adjudicator import adjudicate
from lfa.simulation.outcome_analyzer import analyze_outcomes

__all__ = [
    "load_personas",
    "generate_case",
    "run_arena",
    "adjudicate",
    "analyze_outcomes",
]
