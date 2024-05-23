"""General for the PynyHTM wrapper."""

import pynyhtm


def test_library_licence():
    """Test is license is present in binary library."""
    assert any(x in pynyhtm.lib_get_license() for x in ["Copyright", "Caltech"])
