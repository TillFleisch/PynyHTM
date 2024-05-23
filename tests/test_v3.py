"""Vector v3 related (wrapped) tests for the PynyHTM wrapper."""

import pynyhtm
import pytest
from pynyhtm import V3, SphericalCoordinate


@pytest.mark.parametrize("x, y, z", [(10, 10, 10), (1, 5, 10), (10, 5, 1), (-10, -5, -1)])
def test_v3_init_wrapped_valid(x: float, y: float, z: float):
    """Test instantiation of valid v3 using wrapping method."""
    v3 = pynyhtm.htm_v3_init_wrapped(x, y, z)
    assert v3.x == x and v3.y == y and v3.z == z


def test_v3_to_sc_wrapped():
    """Tests wrapped conversion from v3 vector to spherical coordinates."""
    v3 = V3(1, 1, 1)
    sc = v3.to_sc()
    assert sc.latitude != 0 and sc.longitude != 0


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
    sc = SphericalCoordinate(latitude, longitude)
    v3 = sc.to_v3()
    id = v3.get_htm_id(level)
    assert id == target_id


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
def test_htm_v3_add_wrapped(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float):
    """Tests addition of v3 vectors."""
    res = V3(x1, y1, z1).add(V3(x2, y2, z2))
    assert res.x == x1 + x2 and res.y == y1 + y2 and res.z == z1 + z2

    res = V3(x1, y1, z1) + V3(x2, y2, z2)
    assert res.x == x1 + x2 and res.y == y1 + y2 and res.z == z1 + z2


def test_htm_v3_add_wrapped_invalid():
    """Test invalid type for add instruction."""
    with pytest.raises(TypeError):
        V3(0, 0, 0).add("string")


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
def test_htm_v3_sub_wrapped(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float):
    """Tests subtraction of v3 vectors."""
    res = V3(x1, y1, z1).sub(V3(x2, y2, z2))
    assert res.x == x1 - x2 and res.y == y1 - y2 and res.z == z1 - z2

    res = V3(x1, y1, z1) - V3(x2, y2, z2)
    assert res.x == x1 - x2 and res.y == y1 - y2 and res.z == z1 - z2


def test_htm_v3_sub_wrapped_invalid():
    """Test invalid type for vector subtraction."""
    with pytest.raises(TypeError):
        V3(0, 0, 0).sub("string")


@pytest.mark.parametrize(
    "x, y, z",
    [
        (0, 0, 0),
        (1, 1, 1),
        (1, 2, 3),
        (-1, -2, 3),
    ],
)
def test_htm_v3_neg_wrapped(x: float, y: float, z: float):
    """Tests the negation of vectors."""
    res = V3(x, y, z).neg()
    assert res.x == -x and res.y == -y and res.z == -z

    res = -V3(x, y, z)
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
def test_htm_v3_mul_wrapped(x: float, y: float, z: float, scalar: float):
    """Tests the scalar multiplication of vectors."""
    v = V3(x, y, z)

    res = v.mul(scalar)
    assert res.x == x * scalar and res.y == y * scalar and res.z == z * scalar

    res = v * scalar
    assert res.x == x * scalar and res.y == y * scalar and res.z == z * scalar


def test_htm_v3_mul_wrapped_invalid():
    """Test invalid type for scalar multiplication."""
    with pytest.raises(TypeError):
        V3(0, 0, 0).mul(V3(1, 1, 1))


@pytest.mark.parametrize(
    "x, y, z, scalar",
    [
        (0, 0, 0, 10),
        (1, 1, 1, 2.5),
        (1, 1, 1, 2.0),
        (1, 2, 3, 3.14),
        (-1, -2, 3, 3.0),
    ],
)
def test_htm_v3_div_wrapped(x: float, y: float, z: float, scalar: float):
    """Tests the scalar division of vectors."""
    v = V3(x, y, z)

    res = v.div(scalar)
    assert res.x == x / scalar and res.y == y / scalar and res.z == z / scalar

    res = v / scalar
    assert res.x == x / scalar and res.y == y / scalar and res.z == z / scalar


def test_htm_v3_div_wrapped_invalid():
    """Test invalid type/value for scalar division instruction."""
    with pytest.raises(TypeError):
        V3(0, 0, 0).div(V3(1, 1, 1))

    with pytest.raises(ValueError):
        V3(0, 0, 0).div(0.0)
        V3(1, 1, 1).div(0)
