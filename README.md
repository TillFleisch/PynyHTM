# PynyHTM

PynyHTM is a Cython based Python wrapper for [libtinyhtm](https://github.com/Caltech-IPAC/libtinyhtm/), the minimalistic hierarchal triangular mesh library.
*libtinyhtm*, developed by *Serge Monkewitz* and *Walter Landry* is based on prior work from *Alex Szalay*, *Gyorgy Fekete* and *Jim Gray* in [Searchable Sky Coverage of Astronomical Observations: Footprints and Exposures](https://doi.org/10.48550/arXiv.1005.2606) and [Indexing the Sphere with the Hierarchical Triangular Mesh](https://doi.org/10.48550/arXiv.cs/0701164).

Hierarchal triangular meshes(HTM) use the sub-division of triangles, which are projected onto a sphere, to elegantly and efficiently partition the earth or the sky into regions with different identifiers.

## Usage sample

The code snippets below are available in [this example file](example.py).
Classes `SphericalCoordinate` and `V3` cover basic functionality for expressing points in 3D space.

```python
from PynyHTM import HTM, SphericalCoordinate, Triangle, V3

# Retrieve HTM ID for a spherical coordinate
sc_1 = SphericalCoordinate(10.1234, -20.1234)
id = sc_1.get_htm_id(level=14)
print(f"HTM-ID for sc_1: {id} at level 14")
# >>> HTM-ID for sc_1: 3278525534 at level 14

# Convert spherical coordinate to vector
v_1 = sc_1.to_v3()

# Retrieve HTM ID for a V3 vector
v_2 = V3(0.1,0.2,0.3)
id = v_2.get_htm_id(level=3)
print(f"HTM-ID for v_2: {id} at level 3")
# >>> HTM-ID for v_2: 986 at level 3

# Conversion from vector to spherical coordinate
sc_2 = v_2.to_sc()

diff = sc_1.angle_separation(sc_2)
print(f"Angle between sc_1 and sc_2 (v2): {diff}")
# >>> Angle between sc_1 and sc_2 (v2): 78.05738774142326
```

Triangles, instantiated from the `Triangle` class provide additional information about a trixel within the HTM. They contain the three vertices which make up a Trixel as well as the center and more additional information.

```python
# Retrieve additional information about a triangle within the HTM
triangle = Triangle.from_id(id)
print(f"This triangle is in level {triangle.level}")
# >>> This triangle is in level 3

sc_center = triangle.center.to_sc()
print(f"The center is located at {sc_center}")
# >>> The center is located at SphericalCoordinate({'_latitude': 57.03662706265828, '_longitude': 59.20954536171413})
```

The `HTM` class contains more helpers to manage HTM identifiers.

```python

print(f"The Triangle with id {id} is located at level {HTM.get_level(id)}")
# >>> The Triangle with id 986 is located at level 3

print(f"The ID can also be expressed in it's subdivision form: {HTM.id_to_dec(id)}")
# >>> The ID can also be expressed in it's subdivision form: 23122

# Determine the children of a given triangle
children = HTM.children(id)
print(f"Children of {id}: {children}")
# >>> Children of 986: [3944, 3945, 3946, 3947]

# Determine the parent of a given id
parent = HTM.parent(id)
print(f"Parent of {id}: {parent}")
# >>> Parent of 986: 246

# Determine neighbors of a given triangle
neighbors = HTM.neighbors(id)
print(f"The neighbors of {id} are: {neighbors}")
# >>> The neighbors of 986 are: [987, 988, 1017]

# Search IDs within a circle around a given point
ids = HTM.circle_search(center=v_1, radius=0.5, level=7)
print(f"{ids} are located near center with radius 0.5")
# >>> [200104, 200105, 200106, 200107, 200108, 200134] are located near center with radius 0.5
```
