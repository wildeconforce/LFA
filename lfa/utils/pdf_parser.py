"""PDF parsing utilities.

Strategy: text extraction first (fast path); fall back to OCR for
image-only pages.

Korean Tesseract data (tessdata_best/kor.traineddata) must be
installed for OCR. See docs/SETUP.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class PageText:
    page_number: int  # 1-indexed
    text: str
    method: str       # "text" | "ocr"


def extract_pages(pdf_path: str | Path, ocr_threshold: int = 80) -> list[PageText]:
    """Extract text from each page of a PDF.

    Args:
        pdf_path: Path to PDF.
        ocr_threshold: If a page's direct text extraction yields fewer
            than this many non-boilerplate characters, fall back to OCR.

    Returns:
        A list of `PageText` per page in order.

    Note:
        Skeleton implementation — TODO. Production version uses pymupdf
        for text extraction and pytesseract+kor for OCR fallback.
    """
    raise NotImplementedError("extract_pages not yet implemented (skeleton)")
