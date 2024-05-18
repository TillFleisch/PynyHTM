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


@pytest.mark.parametrize("x, y, z", [(10, 10, 10), (1, 5, 10), (10, 5, 1), (-10, -5, -1)])
def test_v3_init_raw_valid(x: float, y: float, z: float):
    """Test instantiation of valid v3 using raw function."""
    ec, v3 = PynyHTM.htm_v3_init_raw(x, y, z)
    assert ec == 0
    assert v3.get("x") == x and v3.get("y") == y and v3.get("z") == z


@pytest.mark.parametrize("x, y, z", [(10, 10, 10), (1, 5, 10), (10, 5, 1), (-10, -5, -1)])
def test_v3_init_wrapped_valid(x: float, y: float, z: float):
    """Test instantiation of valid v3 using wrapping method."""
    ec, v3 = PynyHTM.htm_v3_init_wrapped(x, y, z)
    assert ec == PynyHTM.Errorcode.HTM_OK
    assert v3.x == x and v3.y == y and v3.z == z


def test_v3_to_sc_raw():
    """Tests v3 vector conversion to spherical coordinates."""
    _, v3 = PynyHTM.htm_v3_init_raw(1, 1, 1)
    ec, sc = PynyHTM.htm_v3_to_sc_raw(v3)
    assert ec == 0
    assert sc.get("lat") != 0 and sc.get("lon") != 0


def test_sc_to_v3_wrapped():
    """Test wrapped conversion from spherical coordinates to v3."""
    sc = PynyHTM.SphericalCoordinate(10, 10)
    ec, v3 = sc.to_v3()
    assert ec == PynyHTM.Errorcode.HTM_OK
    assert v3.x != 0 and v3.y != 0 and v3.z != 0


def test_sc_to_v3_raw():
    """Tests vector conversion from spherical coordinates."""
    _, sc = PynyHTM.htm_sc_init_raw(10, 10)
    ec, v3 = PynyHTM.htm_sc_to_v3_raw(sc)
    assert ec == 0
    assert v3.get("x") != 0 and v3.get("y") != 0 and v3.get("z") != 0


def test_v3_to_sc_wrapped():
    """Tests wrapped conversion from v3 vector to spherical coordinates."""
    v3 = PynyHTM.V3(1, 1, 1)
    ec, sc = v3.to_sc()
    assert ec == PynyHTM.Errorcode.HTM_OK
    assert sc.latitude != 0 and sc.longitude != 0
