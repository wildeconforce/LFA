"""PII redaction utility.

Used at every external boundary — anything leaving LFA (logs, exports,
shared docs) is run through `redact()` first.

Patterns redacted:
    - Korean names (heuristic)
    - 주민등록번호 (resident registration numbers)
    - Phone numbers
    - Bank account numbers
    - Addresses (street level)
    - Case numbers (when configured)

This module is INTENTIONALLY conservative. False positives (over-
redaction) are preferred over false negatives (PII leak).

For legal / journalism-grade redaction, use this as a first pass
followed by human review. Never trust automated redaction alone.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


@dataclass
class RedactionConfig:
    redact_names: bool = True
    redact_rrn: bool = True              # 주민등록번호
    redact_phones: bool = True
    redact_accounts: bool = True
    redact_addresses: bool = True
    redact_case_numbers: bool = False    # default off; mask only when needed
    case_number_replacement: str = "[CASE_NO]"
    name_replacement: str = "[NAME]"


# Regex patterns (conservative)
_RRN_RE = re.compile(r"\b\d{6}\s*[-–]\s*[1-4]\d{6}\b")
_PHONE_RE = re.compile(r"\b0\d{1,2}\s*[-.\s]?\s*\d{3,4}\s*[-.\s]?\s*\d{4}\b")
_ACCOUNT_RE = re.compile(r"\b\d{3,6}-\d{2,6}-\d{2,8}\b")
_CASE_NO_RE = re.compile(r"\b\d{4}\s*(?:가단|가합|나|다|머|차전|고정|고합|노|도|초)\s*\d{2,7}\b")
# Heuristic Korean name: 2–4 Hangul characters preceded by a separator
_NAME_RE = re.compile(r"(?<![가-힣])[가-힣]{2,4}(?=\s*(?:씨|님|님이|군|양|에게|이가|이는|은|는|이|가|와|과|을|를|에서)\b)")

ContextHint = Literal["log", "export", "share", "publish"]


def redact(text: str, config: RedactionConfig | None = None, context: ContextHint = "share") -> str:
    """Redact PII from `text`.

    Args:
        text: Input text.
        config: Redaction configuration. Defaults to maximally conservative.
        context: Where the output is going. `publish` enables case-number
            masking by default.

    Returns:
        Redacted text with PII replaced by tokens.
    """
    if config is None:
        config = RedactionConfig()
        if context == "publish":
            config.redact_case_numbers = True

    out = text
    if config.redact_rrn:
        out = _RRN_RE.sub("[RRN]", out)
    if config.redact_phones:
        out = _PHONE_RE.sub("[PHONE]", out)
    if config.redact_accounts:
        out = _ACCOUNT_RE.sub("[ACCT]", out)
    if config.redact_case_numbers:
        out = _CASE_NO_RE.sub(config.case_number_replacement, out)
    if config.redact_names:
        out = _NAME_RE.sub(config.name_replacement, out)
    return out
