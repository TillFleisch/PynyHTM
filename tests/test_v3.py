"""Vector v3 related (wrapped) tests for the PynyHTM wrapper."""

import pytest

import PynyHTM


@pytest.mark.parametrize("x, y, z", [(10, 10, 10), (1, 5, 10), (10, 5, 1), (-10, -5, -1)])
def test_v3_init_wrapped_valid(x: float, y: float, z: float):
    """Test instantiation of valid v3 using wrapping method."""
    v3 = PynyHTM.htm_v3_init_wrapped(x, y, z)
    assert v3.x == x and v3.y == y and v3.z == z


def test_v3_to_sc_wrapped():
    """Tests wrapped conversion from v3 vector to spherical coordinates."""
    v3 = PynyHTM.V3(1, 1, 1)
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
    sc = PynyHTM.SphericalCoordinate(latitude, longitude)
    v3 = sc.to_v3()
    id = v3.get_htm_id(level)
    assert id == target_id
