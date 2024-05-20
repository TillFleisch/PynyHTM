"""Spherical coordinate related (wrapped) tests for the PynyHTM wrapper."""

import pytest

import PynyHTM


@pytest.mark.parametrize("lat, lon", [(0, 0), (10, 10), (5, 10), (10, 5), (-10, -10)])
def test_sc_init_wrapped_valid(lat: float, lon: float):
    """Test instantiation of valid sc using wrapping method."""
    sc = PynyHTM.htm_sc_init_wrapped(lat, lon)
    assert sc.longitude == lon and sc.latitude == lat


@pytest.mark.parametrize("lat, lon", [(-97, 0), (-100, 0), (-100, -100)])
def test_sc_init_wrapped_invalid(lat: float, lon: float):
    """Test instantiation of invalid sc using wrapping method."""
    with pytest.raises(ValueError):
        PynyHTM.htm_sc_init_wrapped(lat, lon)


def test_sc_to_v3_wrapped():
    """Test wrapped conversion from spherical coordinates to v3."""
    sc = PynyHTM.SphericalCoordinate(10, 10)
    v3 = sc.to_v3()
    assert v3.x != 0 and v3.y != 0 and v3.z != 0


@pytest.mark.parametrize(
    "latitude, longitude, level, target_id",
    [
        (51.7444480, 10.6862911, 0, 15),
        (51.7444480, 10.6862911, 3, 980),
        (51.7444480, 10.6862911, 8, 1003971),
        (51.7444480, 10.6862911, 20, 16843849991222),
    ],
)
def test_sc_to_id_wrapped(latitude: float, longitude: float, level: float, target_id: int):
    """Tests trixel id wrapping using the spherical coordinate class."""
    sc = PynyHTM.SphericalCoordinate(latitude, longitude)
    id = sc.get_htm_id(level)
    assert id == target_id
