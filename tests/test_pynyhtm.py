"""Tests for the PynyHTM wrappers."""

import pytest

import PynyHTM


def test_library_licence():
    """Test is license is present in binary library."""
    assert any(x in PynyHTM.lib_get_license() for x in ["Copyright", "Caltech"])


@pytest.mark.parametrize("lat, lon", [(0, 0), (10, 10), (5, 10), (10, 5), (-10, -10)])
def test_sc_init_raw_valid(lat: float, lon: float):
    """Test instantiation of valid sc using raw function."""
    ec, sc = PynyHTM.htm_sc_init_raw(lat, lon)
    assert ec == 0
    assert sc.get("lon") == lon and sc.get("lat") == lat


@pytest.mark.parametrize("lat, lon", [(0, 0), (10, 10), (5, 10), (10, 5), (-10, -10)])
def test_sc_init_wrapped_valid(lat: float, lon: float):
    """Test instantiation of valid sc using wrapping method."""
    ec, sc = PynyHTM.htm_sc_init_wrapped(lat, lon)
    assert ec == PynyHTM.Errorcode.HTM_OK
    assert sc.longitude == lon and sc.latitude == lat


@pytest.mark.parametrize("lat, lon", [(-97, 0), (-100, 0), (-100, -100)])
def test_sc_init_raw_invalid(lat: float, lon: float):
    """Test instantiation of invalid sc using raw function."""
    ec, _ = PynyHTM.htm_sc_init_raw(lat, lon)
    assert ec != 0


@pytest.mark.parametrize("lat, lon", [(-97, 0), (-100, 0), (-100, -100)])
def test_sc_init_wrapped_invalid(lat: float, lon: float):
    """Test instantiation of invalid sc using wrapping method."""
    ec, _ = PynyHTM.htm_sc_init_wrapped(lat, lon)
    assert ec != PynyHTM.Errorcode.HTM_OK


# TODO: add docs?
