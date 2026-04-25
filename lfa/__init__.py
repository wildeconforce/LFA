"""LFA — Legal Framework Analysis.

Modular framework for analyzing Korean civil and criminal cases.

This software does not provide legal advice. All outputs are strategic
reference materials only. Outputs must be reviewed by a licensed attorney
or 법무사 before being relied upon for any litigation action.
"""

__version__ = "0.1.0-dev"

DISCLAIMER = (
    "본 내용은 법률적 조언이 아닌 전략적 참고 자료입니다. "
    "실제 소송 행위 시에는 반드시 변호사 또는 법무사의 검토를 거치시기 바랍니다."
)

DISCLAIMER_EN = (
    "This output is strategic reference material only, not legal advice. "
    "Review by a licensed attorney or 법무사 is required before any "
    "reliance on this output for litigation purposes."
)

__all__ = ["__version__", "DISCLAIMER", "DISCLAIMER_EN"]
