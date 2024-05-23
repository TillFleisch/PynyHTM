"""Geometry related (raw) tests for the PynyHTM wrapper."""

import pynyhtm
import pytest
from pynyhtm import V3, SphericalCoordinate


@pytest.mark.parametrize("lat, lon", [(0, 0), (10, 10), (5, 10), (10, 5), (-10, -10)])
def test_sc_init_raw_valid(lat: float, lon: float):
    """Test instantiation of valid sc using raw function."""
    ec, sc = pynyhtm.htm_sc_init_raw(lat, lon)
    assert ec == 0
    assert sc.get("lon") == lon and sc.get("lat") == lat


@pytest.mark.parametrize("lat, lon", [(-97, 0), (-100, 0), (-100, -100)])
def test_sc_init_raw_invalid(lat: float, lon: float):
    """Test instantiation of invalid sc using raw function."""
    ec, _ = pynyhtm.htm_sc_init_raw(lat, lon)
    assert ec != 0


@pytest.mark.parametrize("x, y, z", [(10, 10, 10), (1, 5, 10), (10, 5, 1), (-10, -5, -1)])
def test_v3_init_raw_valid(x: float, y: float, z: float):
    """Test instantiation of valid v3 using raw function."""
    ec, v3 = pynyhtm.htm_v3_init_raw(x, y, z)
    assert ec == 0
    assert v3.get("x") == x and v3.get("y") == y and v3.get("z") == z


def test_v3_to_sc_raw():
    """Tests v3 vector conversion to spherical coordinates."""
    _, v3 = pynyhtm.htm_v3_init_raw(1, 1, 1)
    ec, sc = pynyhtm.htm_v3_to_sc_raw(v3)
    assert ec == 0
    assert sc.get("lat") != 0 and sc.get("lon") != 0


def test_sc_to_v3_raw():
    """Tests vector conversion from spherical coordinates."""
    _, sc = pynyhtm.htm_sc_init_raw(10, 10)
    ec, v3 = pynyhtm.htm_sc_to_v3_raw(sc)
    assert ec == 0
    assert v3.get("x") != 0 and v3.get("y") != 0 and v3.get("z") != 0


@pytest.mark.parametrize("latitude, longitude", [(10, 0), (15, 0), (20, 20)])
def test_sc_to_v3_to_sc(latitude: float, longitude: float):
    """Tests wrapped conversion from v3 vector to spherical coordinates."""
    sc = SphericalCoordinate(latitude, longitude)
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
    sc = SphericalCoordinate(latitude, longitude)
    v3 = sc.to_v3()
    assert pynyhtm.htm_v3_id_raw(v3.get_htm_v3(), level) == id


@pytest.mark.parametrize(
    "x1, y1, z1, x2, y2, z2",
    [
        (0, 0, 0, 0, 0, 0),
        (1, 1, 1, 0, 0, 0),
        (1, 1, 1, 1, 1, 1),
        (1, 2, 3, 4, 5, 6),
        (-1, 2, -3, -4, -5, 6),
    ],
)
def test_htm_v3_add_raw(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float):
    """Tests addition of v3 vectors."""
    ec, v1 = pynyhtm.htm_v3_init_raw(x1, y1, z1)
    assert ec == 0
    ec, v2 = pynyhtm.htm_v3_init_raw(x2, y2, z2)
    assert ec == 0

    res = pynyhtm.htm_v3_add_raw(v1, v2)
    res = V3.from_htm_v3(res)
    assert res.x == x1 + x2 and res.y == y1 + y2 and res.z == z1 + z2


@pytest.mark.parametrize(
    "x1, y1, z1, x2, y2, z2",
    [
        (0, 0, 0, 0, 0, 0),
        (1, 1, 1, 0, 0, 0),
        (1, 1, 1, 1, 1, 1),
        (1, 2, 3, 4, 5, 6),
        (-1, 2, -3, -4, -5, 6),
    ],
)
def test_htm_v3_sub_raw(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float):
    """Tests subtraction of v3 vectors."""
    ec, v1 = pynyhtm.htm_v3_init_raw(x1, y1, z1)
    assert ec == 0
    ec, v2 = pynyhtm.htm_v3_init_raw(x2, y2, z2)
    assert ec == 0

    res = pynyhtm.htm_v3_sub_raw(v1, v2)
    res = V3.from_htm_v3(res)
    assert res.x == x1 - x2 and res.y == y1 - y2 and res.z == z1 - z2


@pytest.mark.parametrize(
    "x, y, z",
    [
        (0, 0, 0),
        (1, 1, 1),
        (1, 2, 3),
        (-1, -2, 3),
    ],
)
def test_htm_v3_neg_raw(x: float, y: float, z: float):
    """Tests the negation of vectors."""
    ec, v1 = pynyhtm.htm_v3_init_raw(x, y, z)
    assert ec == 0

    res = pynyhtm.htm_v3_neg_raw(v1)
    res = V3.from_htm_v3(res)
    assert res.x == -x and res.y == -y and res.z == -z


@pytest.mark.parametrize(
    "x, y, z, scalar",
    [
        (0, 0, 0, 10),
        (1, 1, 1, 2.5),
        (1, 1, 1, 0),
        (1, 2, 3, 3.14),
        (-1, -2, 3, 0),
    ],
)
def test_htm_v3_mul_raw(x: float, y: float, z: float, scalar: float):
    """Tests the scalar multiplication of vectors."""
    ec, v1 = pynyhtm.htm_v3_init_raw(x, y, z)
    assert ec == 0

    res = pynyhtm.htm_v3_mul_raw(v1, scalar)
    res = V3.from_htm_v3(res)
    assert res.x == x * scalar and res.y == y * scalar and res.z == z * scalar


@pytest.mark.parametrize(
    "x, y, z, scalar",
    [
        (0, 0, 0, 10),
        (1, 1, 1, 2.5),
        (1, 1, 1, 2.0),
        (1, 2, 3, 3.14),
        (-1, -2, 3, 3),
    ],
)
def test_htm_v3_div_raw(x: float, y: float, z: float, scalar: float):
    """Tests the scalar division of vectors."""
    ec, v1 = pynyhtm.htm_v3_init_raw(x, y, z)
    assert ec == 0

    res = pynyhtm.htm_v3_div_raw(v1, scalar)
    res = V3.from_htm_v3(res)
    assert res.x == x / scalar and res.y == y / scalar and res.z == z / scalar


@pytest.mark.parametrize(
    "lat1, lon1, lat2, lon2, target",
    [
        (0, 0, 0, 0, 0),
        (10, 10, 10, 10, 0),
        (0, 0, 0, 90, 90),
        (0, 0, 0, -90, 90),
        (0, 0, 90, 0, 90),
        (0, 0, 0, 180, 180),
        (0, -90, 0, 180, 90),
        (0, 0, 90, 0, 90),
        (-90, -90, 90, 90, 180),
    ],
)
def test_htm_sc_angsep_raw(lat1, lon1, lat2, lon2, target):
    """Test the raw angle distance function for sc."""
    ec, sc1 = pynyhtm.htm_sc_init_raw(lat1, lon1)
    assert ec == 0

    ec, sc2 = pynyhtm.htm_sc_init_raw(lat2, lon2)
    assert ec == 0

    result = pynyhtm.htm_sc_angsep_raw(sc1, sc2)
    assert abs(result - target) < 0.0001
