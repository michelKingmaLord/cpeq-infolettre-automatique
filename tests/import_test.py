"""Test cpeq-infolettre-automatique."""

import pytest

import cpeq_infolettre_automatique


@pytest.mark.parametrize("package_name", [cpeq_infolettre_automatique.__name__])
def test_import(package_name: str) -> None:
    """Test that the package can be imported."""
    assert isinstance(package_name, str), "Package name should be a string"
