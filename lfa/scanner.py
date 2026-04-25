"""Module 1 — CASE_SCANNER.

Parse heterogeneous case-file inputs (PDF, image, DOCX, HWP, plain text)
into a structured `CaseRecord`.

Pipeline:
    1. Format detect (PDF / image / DOCX / HWP / TXT)
    2. Text extract (pdftotext or OCR; python-docx; HWP via pyhwp)
    3. NER + regex for dates, parties, amounts, case numbers
    4. 6하원칙 (who/when/where/what/how/why) structuring
    5. Timeline auto-build with conflict detection hooks

Inputs may include 소장, 답변서, 준비서면, 판결문, 결정문, 녹취록,
서증제출서, 갑/을 호증, 카카오톡/문자 캡처.

Outputs a `CaseRecord` Pydantic model (see `lfa.models.case`).

This module does not produce legal advice. It produces structured fact
extraction. All outputs require human verification before use.
"""

from __future__ import annotations

from pathlib import Path

from lfa.models.case import CaseRecord


def scan_case(case_dir: str | Path) -> CaseRecord:
    """Scan a case directory and produce a structured `CaseRecord`.

    Args:
        case_dir: Directory containing case-file inputs (PDFs, images,
            DOCX, HWP, plain text).

    Returns:
        A `CaseRecord` with parsed parties, timeline, claims, evidence,
        and prior decisions.

    Raises:
        FileNotFoundError: if `case_dir` does not exist.
        ValueError: if no parseable inputs are found.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("CASE_SCANNER not yet implemented (skeleton)")


def scan_document(path: str | Path) -> dict:
    """Parse a single document into a fact dict.

    Note:
        Skeleton implementation — TODO.
    """
    raise NotImplementedError("scan_document not yet implemented (skeleton)")
