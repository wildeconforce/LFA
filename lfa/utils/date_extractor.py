"""Korean date extraction from heterogeneous legal text.

Handles common Korean legal date formats:
    - 2022. 4. 11.
    - 2022. 4. 11. 09:30경
    - 2022년 4월 11일
    - 2022-04-11
    - 22. 4. 11.
"""

from __future__ import annotations

import re
from datetime import date


_PATTERNS = [
    re.compile(r"(\d{4})\s*[.년]\s*(\d{1,2})\s*[.월]\s*(\d{1,2})"),
    re.compile(r"(\d{4})-(\d{2})-(\d{2})"),
    re.compile(r"(?<!\d)(\d{2})\s*[.년]\s*(\d{1,2})\s*[.월]\s*(\d{1,2})"),
]


def extract_dates(text: str) -> list[date]:
    """Extract all Korean-formatted dates from `text` in order of appearance.

    Note:
        Skeleton implementation — TODO. The 2-digit year branch needs
        a sensible century rule (Korean legal docs usually 19xx/20xx).
    """
    raise NotImplementedError("extract_dates not yet implemented (skeleton)")
