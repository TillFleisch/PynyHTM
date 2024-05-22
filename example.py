"""Examples for using PynyHTM."""

from PynyHTM import HTM, V3, SphericalCoordinate, Triangle

if __name__ == "__main__":
    # Retrieve HTM ID for a spherical coordinate
    sc_1 = SphericalCoordinate(10.1234, -20.1234)
    id = sc_1.get_htm_id(level=14)
    print(f"HTM-ID for sc_1: {id} at level 14")

    # Convert spherical coordinate to vector
    v_1 = sc_1.to_v3()

    # Retrieve HTM ID for a V3 vector
    v_2 = V3(0.1, 0.2, 0.3)
    id = v_2.get_htm_id(level=3)
    print(f"HTM-ID for v_2: {id} at level 3")

    # Conversion from vector to spherical coordinate
    sc_2 = v_2.to_sc()

    diff = sc_1.angle_separation(sc_2)
    print(f"Angle between sc_1 and sc_2 (v2): {diff}")

    # Retrieve additional information about a triangle within the HTM
    triangle = Triangle.from_id(id)
    print(f"This triangle is in level {triangle.level}")

    sc_center = triangle.center.to_sc()
    print(f"The center is located at {sc_center}")
    print(f"The Triangle with id {id} is located at level {HTM.get_level(id)}")
    print(f"The ID can also be expressed in it's subdivision form: {HTM.id_to_dec(id)}")

    # Determine the children of a given triangle
    children = HTM.children(id)
    print(f"Children of {id} are: {children}")

    # Determine the parent of a given id
    parent = HTM.parent(id)
    print(f"Parent of {id} is: {parent}")

    # Determine neighbors of a given triangle
    neighbors = HTM.neighbors(id)
    print(f"The neighbors of {id} are: {neighbors}")

    # Search IDs within a circle around a given point
    ids = HTM.circle_search(center=v_1, radius=0.5, level=7)
    print(f"{ids} are located near center with radius 0.5")
