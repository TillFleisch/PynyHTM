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
    sc = PynyHTM.htm_sc_init_wrapped(lat, lon)
    assert sc.longitude == lon and sc.latitude == lat


@pytest.mark.parametrize("lat, lon", [(-97, 0), (-100, 0), (-100, -100)])
def test_sc_init_raw_invalid(lat: float, lon: float):
    """Test instantiation of invalid sc using raw function."""
    ec, _ = PynyHTM.htm_sc_init_raw(lat, lon)
    assert ec != 0


@pytest.mark.parametrize("lat, lon", [(-97, 0), (-100, 0), (-100, -100)])
def test_sc_init_wrapped_invalid(lat: float, lon: float):
    """Test instantiation of invalid sc using wrapping method."""
    with pytest.raises(ValueError):
        PynyHTM.htm_sc_init_wrapped(lat, lon)


@pytest.mark.parametrize("x, y, z", [(10, 10, 10), (1, 5, 10), (10, 5, 1), (-10, -5, -1)])
def test_v3_init_raw_valid(x: float, y: float, z: float):
    """Test instantiation of valid v3 using raw function."""
    ec, v3 = PynyHTM.htm_v3_init_raw(x, y, z)
    assert ec == 0
    assert v3.get("x") == x and v3.get("y") == y and v3.get("z") == z


@pytest.mark.parametrize("x, y, z", [(10, 10, 10), (1, 5, 10), (10, 5, 1), (-10, -5, -1)])
def test_v3_init_wrapped_valid(x: float, y: float, z: float):
    """Test instantiation of valid v3 using wrapping method."""
    v3 = PynyHTM.htm_v3_init_wrapped(x, y, z)
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
    v3 = sc.to_v3()
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
    sc = v3.to_sc()
    assert sc.latitude != 0 and sc.longitude != 0


@pytest.mark.parametrize("latitude, longitude", [(10, 0), (15, 0), (20, 20)])
def test_sc_to_v3_to_sc(latitude: float, longitude: float):
    """Tests wrapped conversion from v3 vector to spherical coordinates."""
    sc = PynyHTM.SphericalCoordinate(latitude, longitude)
    sc = sc.to_v3().to_sc()
    assert abs(sc.latitude - latitude) < 0.001 and abs(sc.longitude - longitude) < 0.001


@pytest.mark.parametrize(
    "latitude, longitude, level, id",
    [
        (51.7444480, 10.6862911, 0, 15),
        (51.7444480, 10.6862911, 3, 980),
        (51.7444480, 10.6862911, 8, 1003971),
        (51.7444480, 10.6862911, 20, 16843849991222),
    ],
)
def test_v3_to_id_raw(latitude: float, longitude: float, level: float, id: int):
    """Tests trixel id wrapping for a given v3 vector."""
    sc = PynyHTM.SphericalCoordinate(latitude, longitude)
    v3 = sc.to_v3()
    assert PynyHTM.htm_v3_id_raw(v3.get_htm_v3(), level) == id


@pytest.mark.parametrize(
    "latitude, longitude, level, target_id",
    [
        (51.7444480, 10.6862911, 0, 15),
        (51.7444480, 10.6862911, 3, 980),
        (51.7444480, 10.6862911, 8, 1003971),
        (51.7444480, 10.6862911, 20, 16843849991222),
    ],
)
def test_v3_to_id_wrapped(latitude: float, longitude: float, level: float, target_id: int):
    """Tests trixel id wrapping using the V3 class."""
    sc = PynyHTM.SphericalCoordinate(latitude, longitude)
    v3 = sc.to_v3()
    id = v3.get_htm_id(level)
    assert id == target_id


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
