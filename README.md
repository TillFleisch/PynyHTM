# PynyHTM

PynyHTM is a Cython based Python wrapper for [libtinyhtm](https://github.com/Caltech-IPAC/libtinyhtm/), the minimalistic hierarchal triangular mesh library.
*libtinyhtm*, developed by *Serge Monkewitz* and *Walter Landry* is based on prior work from *Alex Szalay*, *Gyorgy Fekete* and *Jim Gray* in [Searchable Sky Coverage of Astronomical Observations: Footprints and Exposures](https://doi.org/10.48550/arXiv.1005.2606) and [Indexing the Sphere with the Hierarchical Triangular Mesh](https://doi.org/10.48550/arXiv.cs/0701164).

Hierarchal triangular meshes(HTM) use the sub-division of triangles, which are projected onto a sphere, to elegantly and efficiently partition the earth or the sky into regions with different identifiers.
