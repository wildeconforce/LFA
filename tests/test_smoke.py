"""Smoke tests — verify package imports and disclaimer is intact."""

from __future__ import annotations

import lfa


def test_version_exposed():
    assert hasattr(lfa, "__version__")
    assert isinstance(lfa.__version__, str)


def test_disclaimer_present():
    assert lfa.DISCLAIMER
    assert "법률적 조언" in lfa.DISCLAIMER
    assert "변호사" in lfa.DISCLAIMER or "법무사" in lfa.DISCLAIMER


def test_disclaimer_en_present():
    assert lfa.DISCLAIMER_EN
    assert "legal advice" in lfa.DISCLAIMER_EN


def test_modules_importable():
    """All 14 module files should at least import."""
    import lfa.scanner       # noqa
    import lfa.breaker       # noqa
    import lfa.hunter        # noqa
    import lfa.writer        # noqa
    import lfa.reviewer      # noqa
    import lfa.verifier      # noqa
    import lfa.simulator     # noqa
    import lfa.timeline      # noqa
    import lfa.adversarial   # noqa
    from lfa.simulation import (  # noqa
        persona_loader,
        case_generator,
        arena,
        judge_adjudicator,
        outcome_analyzer,
    )


def test_models_importable():
    from lfa.models import case, persona  # noqa
