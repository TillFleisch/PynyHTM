"""Triangle related tests for the PynyHTM wrapper."""

import random

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


@pytest.mark.parametrize("id, parent_id", [(61, 15), (16062643, 4015660)])
def test_htm_parent(id: int64, parent_id: int64):
    """Test parent id determination."""
    assert PynyHTM.HTM.parent(id) == parent_id


@pytest.mark.parametrize("id", [(-1), (123), (15)])
def test_htm_parent_invalid(id: int64):
    """Test invalid id for parent determination."""
    with pytest.raises(ValueError):
        assert PynyHTM.HTM.parent(id)


@pytest.mark.parametrize("id", [(61), (15), (16062643), (4015660)])
def test_htm_children(id: int64):
    """Validate generated children are valid."""
    children = PynyHTM.HTM.children(id)

    # Instantiate child to verify it's id is correct
    for child in children:
        assert Triangle.from_id(child) is not None


@pytest.mark.parametrize("id", [(123), (-1)])
def test_htm_children_invalid(id: int64):
    """Test invalid id during child generation."""
    with pytest.raises(ValueError):
        PynyHTM.HTM.children(id)


@pytest.mark.parametrize(
    "id, dir, target_id",
    [
        # N3 (15)
        # west side
        (15634, 2, 12577),
        (12676, 1, 15688),
        (16004, 1, 12360),
        (12306, 2, 15905),
        # bottom side
        (15896, 2, 8228),
        (8338, 2, 15969),
        (15494, 2, 8777),
        (8722, 2, 15393),
        # east side
        (15385, 1, 14886),
        (14980, 1, 15432),
        (15748, 1, 14664),
        (14610, 2, 15649),
        # S0 (8)
        # west side
        (8216, 2, 11812),
        (11928, 2, 8292),
        (8582, 2, 11593),
        (11616, 2, 8592),
        # east side
        (8464, 1, 9504),
        (9606, 2, 8521),
        (8836, 1, 9288),
        (9241, 1, 8742),
        # top side covered by N3(15)
        # S1 (9) / N2 (14)
        (9224, 2, 14852),
        (14921, 1, 9350),
        (14374, 2, 9753),
        (9828, 1, 14488),
        # sides covered by other root triangles
        # S3 (11) / N0 (12)
        (12324, 1, 11800),
        (11876, 1, 12440),
        (12897, 1, 11410),
        (11273, 1, 12806),
        #  N1 (13)
        # east side
        (13574, 2, 14601),
        (14744, 2, 13668),
        (13977, 1, 14438),
        (14340, 1, 13832),
        # bottom side
        (13348, 1, 10776),
        (10854, 2, 13465),
        (13924, 1, 10392),
        (10276, 1, 13848),
        # west side
        (13318, 2, 12809),
        (12953, 1, 13414),
        (12616, 2, 13700),
        (13606, 2, 12569),
        # S2 (10)
        # east side
        (9736, 2, 10244),
        (10340, 1, 9880),
        (9544, 2, 10628),
        (10529, 1, 9490),
        # west side
        (10520, 2, 11556),
        (11672, 2, 10596),
        (10905, 1, 11366),
        (11268, 1, 10760),
        # sides covered by other root triangles
    ],
)
def test_directional_neighbor(id: int64, dir: int, target_id: int64):
    """Test if the correct neighbor is retrieved across root level changes."""
    if dir == 0:
        dir = PynyHTM.NeighborDirection.OC_ZERO
    elif dir == 1:
        dir = PynyHTM.NeighborDirection.OC_ONE
    elif dir == 2:
        dir = PynyHTM.NeighborDirection.OC_TWO

    neighbor = PynyHTM.HTM.neighbor(id, dir)[0]
    assert neighbor == target_id


@pytest.mark.parametrize(
    "id, n1, n2, n3",
    [
        # 3 - center
        (53183, 53180, 53181, 53182),  # upright
        (53175, 53173, 53172, 53174),  # upside down
        # 0 - edge
        (53180, 53173, 53183, 53178),  # upright
        (53168, 53171, 53140, 53160),  # upside down
        # 1 - edge
        (53181, 53183, 53170, 53177),  # upright
        (53173, 53180, 53130, 53175),  # upside down
        # 2 - edge
        (53182, 53174, 53169, 53183),  # upright
        (53178, 53125, 53179, 53180),  # upside down
    ],
)
def test_neighbors(id: int64, n1: int64, n3: int64, n2: int64):
    """Test if the correct neighbors are retrieved."""
    neighbors = PynyHTM.HTM.neighbors(id)

    assert n1 in neighbors
    assert n2 in neighbors
    assert n3 in neighbors


def test_neighbors_fuzz():
    """Test neighbor generation using symmetry property with random samples."""
    samples = 10000
    for _ in range(0, samples):
        layer = random.randrange(1, 20)
        id_prefix = random.choice([x for x in range(8, 16)])
        id_suffix = random.getrandbits((layer - 1) * 2)
        id = id_prefix << (layer * 2) | id_suffix

        # Test using neighbor symmetry
        neighbors = PynyHTM.HTM.neighbors(id)
        for neighbor in neighbors:
            back_neighbors = PynyHTM.HTM.neighbors(neighbor)
            assert id in back_neighbors
