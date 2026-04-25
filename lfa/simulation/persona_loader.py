"""Module 9 — PERSONA_LOADER.

Load synthetic Korean personas from NVIDIA Nemotron-Personas-Korea
into a queryable local index.

Source dataset:
    https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea

    6M synthetic Korean personas grounded in KOSIS statistics + Supreme
    Court case data. PII-zero, PIPA-compliant.

Local index: SQLite, indexed on age, gender, occupation, region, and
financial state for fast filtered sampling.

This module produces only synthetic personas. Real-world persona data
must NEVER be loaded through this interface.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from lfa.models.persona import Persona, JudgePersona, CounselPersona


PersonaRole = Literal[
    "party",        # 일반 당사자 (원고/피고)
    "judge_1",      # 1심 판사
    "judge_2",      # 2심 판사
    "attorney",     # 변호사
    "prosecutor",   # 검사
    "witness",      # 증인
]


def load_personas(
    role: PersonaRole,
    count: int = 1,
    constraints: dict | None = None,
    seed: int = 42,
) -> list[Persona]:
    """Load synthetic personas for a role.

    Args:
        role: Which role to populate.
        count: Number of personas to return.
        constraints: Optional filter dict (e.g. `{"age": (40, 60)}`).
        seed: RNG seed for reproducibility.

    Returns:
        A list of `Persona` (or specialized subtype for judge / counsel).

    Note:
        Skeleton implementation — TODO. Production version downloads
        Nemotron-Personas-Korea, builds a SQLite index, and samples
        with constraint filters.
    """
    raise NotImplementedError("PERSONA_LOADER not yet implemented (skeleton)")


def build_index(dataset_path: str | Path, db_path: str | Path) -> None:
    """One-time: download Nemotron-Personas-Korea and build SQLite index.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("build_index not yet implemented (skeleton)")
