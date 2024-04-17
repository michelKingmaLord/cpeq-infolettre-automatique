"""Test cpeq-infolettre-automatique."""

import cpeq_infolettre_automatique


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(cpeq_infolettre_automatique.__name__, str)
