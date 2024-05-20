"""General for the PynyHTM wrapper."""

import PynyHTM


def test_library_licence():
    """Test is license is present in binary library."""
    assert any(x in PynyHTM.lib_get_license() for x in ["Copyright", "Caltech"])
