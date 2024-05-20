"""Triangle related tests for the PynyHTM wrapper."""

import pytest
from numpy import int64

import PynyHTM
from PynyHTM import Triangle


@pytest.mark.parametrize("id, level", [(15, 0), (980, 3), (1003971, 8), (16843849991222, 20)])
def test_htm_tri_init_raw(id: int64, level: int):
    """Test instantiation of htm_tri struct for an id."""
    ec, htm_tri = PynyHTM.htm_tri_init_raw(id)
    assert ec == 0

    assert htm_tri is not None
    assert htm_tri.get("center") is not None
    assert htm_tri.get("level") == level


@pytest.mark.parametrize("id, level", [(15, 0), (980, 3), (1003971, 8), (16843849991222, 20)])
def test_htm_tri_init_wrapped(id: int64, level: int):
    """Test instantiation of htm_tri struct for an id."""
    triangle = Triangle.from_id(id)
    assert triangle is not None
    assert triangle.center is not None
    assert triangle.level == level
    assert len(triangle.vertices) == 3


@pytest.mark.parametrize("id", [(0), (-1)])
def test_htm_tri_init_wrapped_invalid(id: int64):
    """Test instantiation of htm_tri struct with invalid ids."""
    with pytest.raises(ValueError):
        Triangle.from_id(id)


@pytest.mark.parametrize("id, level", [(15, 0), (980, 3), (1003971, 8), (16843849991222, 20)])
def test_htm_level_raw(id: int, level: int):
    """Test id to level conversion."""
    assert PynyHTM.htm_level_raw(id) == level
    assert PynyHTM.HTM.get_level(id) == level


@pytest.mark.parametrize("id", [(0), (-1)])
def test_htm_level_raw_invalid(id: int):
    """Test invalid id during level conversion."""
    with pytest.raises(ValueError):
        PynyHTM.htm_level_raw(id)
    with pytest.raises(ValueError):
        PynyHTM.HTM.get_level(id)


def test_htm_id_to_dec():
    """Test if htm_idtodec is wrapped."""
    assert PynyHTM.htm_id_to_dec(12345) > 0
    assert PynyHTM.HTM.id_to_dec(12345) > 0
