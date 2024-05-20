"""Wrapping classes and methods for libtinyhtm."""
from enum import Enum
from numpy cimport int64_t


cdef extern from "libtinyhtm/src/licence.cxx":
    const char* get_license()


def lib_get_license() -> str:
    """Retrieves the licence from the compiled library."""
    cdef const char* license = get_license()
    return license.decode("utf-8")


cdef extern from "libtinyhtm/src/tinyhtm/common.h":
    ctypedef enum htm_errcode:
        HTM_OK = 0
        HTM_ENULLPTR
        HTM_ENANINF
        HTM_EZERONORM
        HTM_ELAT
        HTM_EANG
        HTM_EHEMIS
        HTM_ELEN
        HTM_EDEGEN
        HTM_EID
        HTM_ELEVEL
        HTM_EIO
        HTM_EMMAN
        HTM_EINV
        HTM_ETREE
        HTM_NUM_CODES


class Errorcode(Enum):
    """Errorcodes used by libtinyhtm."""
    HTM_OK = 0
    HTM_ENULLPTR = 1
    HTM_ENANINF = 2
    HTM_EZERONORM = 3
    HTM_ELAT = 4
    HTM_EANG = 5
    HTM_EHEMIS = 6
    HTM_ELEN = 7
    HTM_EDEGEN = 8
    HTM_EID = 9
    HTM_ELEVEL = 10
    HTM_EIO = 11
    HTM_EMMAN = 12
    HTM_EINV = 13
    HTM_ETREE = 14
    HTM_NUM_CODES = 15


cdef extern from "libtinyhtm/src/tinyhtm/geometry.h":
    struct htm_sc:
        double lon
        double lat

    struct htm_v3:
        double x
        double y
        double z

    htm_errcode htm_sc_init(htm_sc *out, double lon_deg, double lat_deg)

    htm_errcode htm_v3_init(htm_v3 *out, double x, double y, double z)

    htm_errcode htm_sc_tov3(htm_v3 *out, const htm_sc *p)

    htm_errcode htm_v3_tosc(htm_sc *out, const htm_v3 *v)

    void htm_v3_add(htm_v3 *out, const htm_v3 *v1, const htm_v3 *v2)

    void htm_v3_sub(htm_v3 *out, const htm_v3 *v1, const htm_v3 *v2)

    void htm_v3_neg(htm_v3 *out, const htm_v3 *v)

    void htm_v3_mul(htm_v3 *out, const htm_v3 *v, double s)

    void htm_v3_div(htm_v3 *out, const htm_v3 *v, double s)

    double htm_sc_angsep(const htm_sc *p1, const htm_sc *p2)


class SphericalCoordinate():
    """Wrapping class for the htm_sc struct."""

    @property
    def latitude(self) -> float:
        """Latitude of this spherical coordinate."""
        return self._latitude

    @property
    def longitude(self) -> float:
        """Longitude of this spherical coordinate."""
        return self._longitude

    def __init__(self, latitude: float, longitude: float) -> None:
        """
        Initializes this spherical coordinate with given latitude and longitude.

        :param latitude: latitude of the spherical coordinate
        :param longitude: longitude of the spherical coordinate
        """
        self._latitude=latitude
        self._longitude=longitude

    def __repr__(self):
        """Detailed representation of this SphericalCoordinate."""
        return f"SphericalCoordinate({str(self.__dict__)})"

    def get_htm_sc(self):
        """Gets a htm_sc strcut based on this spherical coordinate."""
        return htm_sc(self._longitude, self._latitude)

    def from_htm_sc(sc: htm_sc) -> SphericalCoordinate:
        """
        Creates a Spherical coordinate based on a htm_sc struct.

        :param sc: htm_sc struct which contains the latitude and longitude
        :returns: A SphericalCoordinate object with values from the provided htm_sc struct
        :raises valueError: if the provided spherical coordinate struct object is invalid
        """
        try:
            latitude=sc.get("lat")
            longitude=sc.get("lon")
            return SphericalCoordinate(latitude=latitude, longitude=longitude)
        except Exception:
            raise ValueError(f"{sc} does not have lat,lon attribute.")

    def to_v3(self) -> V3:
        """
        Transforms this spherical coordinate into a v3 vector.

        :return: v3 equivalent
        :raises valueError: if conversation failed
        """
        ec, v3 = htm_sc_to_v3_raw(self.get_htm_sc())
        if Errorcode(ec) != Errorcode.HTM_OK:
            raise ValueError(f"Conversion to V3 failed: {ec}")
        return V3.from_htm_v3(v3)

    def angle_separation(self, other: SphericalCoordinate) -> float:
        """
        Determine the angle difference between the two given spherical coordinates.

        :param other: second reference point
        :returns: angle between sc1 and sc2
        """
        return htm_sc_angsep_raw(self.get_htm_sc(), other.get_htm_sc())

    def get_htm_id(self, level: int) -> int64_t:
        """Gets the HTM id for this spherical coordinate at the given level.

        :param level: depth at which the id should be determined.
        :returns: id of the trixel in which this spherical coordinate lands
        :raises valueError: if the provided htm_v3 struct object is invalid
        """
        return self.to_v3().get_htm_id(level)


class V3():
    """Wrapping class for the v3 struct (vector)."""

    @property
    def x(self) -> float:
        """X coordinate of this vector."""
        return self._x

    @property
    def y(self) -> float:
        """Y coordinate of this vector."""
        return self._y

    @property
    def z(self) -> float:
        """Z coordinate of this vector."""
        return self._z

    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Initializes this v3 vector with the given values.

        :param x: x (first) value
        :param y: y (second) value
        :param z: z (third) value
        """
        self._x=x
        self._y=y
        self._z=z

    def __repr__(self):
        """Detailed representation of this V3 Vector."""
        return f"V3({str(self.__dict__)})"

    def get_htm_v3(self):
        """Gets a htm_v3 strcut based on this v3 object."""
        return htm_v3(self._x, self._y, self._z)

    def from_htm_v3(v3: htm_v3) -> V3:
        """
        Creates a V3 object based on a htm_v3 struct.

        :param v3: htm_v3 struct which contains x,y,z
        :returns: A V3 object with values from the provided htm_v3 struct
        :raises valueError: if the provided htm_v3 struct object is invalid
        """
        try:
            x=v3.get("x")
            y=v3.get("y")
            z=v3.get("z")
            return V3(x=x, y=y, z=z)
        except Exception:
            raise ValueError(f"{v3} does not have x,y,z attributes.")

    def to_sc(self) -> SphericalCoordinate:
        """
        Transforms this V3 vector into a sphercial coordinate.

        :returns: Spherical coordinate equivalent
        :raises valueError: if conversion failed
        """
        ec, sc = htm_v3_to_sc_raw(self.get_htm_v3())
        if Errorcode(ec) != Errorcode.HTM_OK:
            raise ValueError(f"Conversion to SC failed: {ec}")
        return SphericalCoordinate.from_htm_sc(sc)

    def get_htm_id(self, level: int) -> int64_t:
        """Gets the HTM id for this v3 vector at the given level.

        :param level: depth at which the id should be determined.
        :returns: id of the trixel in which this v3 lands
        """

        return htm_v3_id_raw(self.get_htm_v3(), level)

    def add(self, other: V3) -> V3:
        """
        Adds the other vector to this vector.

        :param other: vector to add
        :returns: self + vector
        """
        if not isinstance(other, V3):
            raise TypeError(f"Cannot add {type(other)} to V3")

        result = htm_v3_add_raw(self.get_htm_v3(), other.get_htm_v3())
        return V3.from_htm_v3(result)

    def __add__(self, other: V3) -> V3:
        return self.add(other)

    def sub(self, other: V3) -> V3:
        """
        Subtracts other from this vector.

        :param other: vector to subtract
        :returns: self - vector
        """
        if not isinstance(other, V3):
            raise TypeError(f"Cannot subtract {type(other)} from")

        result = htm_v3_sub_raw(self.get_htm_v3(), other.get_htm_v3())
        return V3.from_htm_v3(result)

    def __sub__(self, other: V3) -> V3:
        return self.sub(other)

    def neg(self) -> V3:
        """
        Negates this vector.

        :returns: vector with inverted components
        """
        result = htm_v3_neg_raw(self.get_htm_v3())
        return V3.from_htm_v3(result)

    def __neg__(self) -> V3:
        return self.neg()

    def mul(self, scalar: float) -> V3:
        """
        Scalar multiplication with this v3.

        :param scalar: scalar
        :returns: self * scalar
        """
        if not isinstance(scalar, float):
            raise TypeError(f"Cannot multiply V3 with {type(scalar)}")

        result = htm_v3_mul_raw(self.get_htm_v3(), scalar)
        return V3.from_htm_v3(result)

    def __mul__(self, scalar: float) -> V3:
        return self.mul(scalar)

    def div(self, scalar: float) -> V3:
        """
        Scalar division with this v3.

        :param scalar: scalar divisor
        :returns: self / scalar
        """
        if not isinstance(scalar, float):
            raise TypeError(f"Cannot divide V3 by {type(scalar)}")

        if scalar == 0:
            raise ValueError(f"Cannot divide by {scalar}")

        result = htm_v3_div_raw(self.get_htm_v3(), scalar)
        return V3.from_htm_v3(result)

    def __truediv__(self, scalar: float) -> V3:
        return self.div(scalar)


def htm_sc_init_raw(latitude: float, longitude: float) -> tuple[htm_errcode, htm_sc]:
    """
    Wraps htm_sc_init, instantiates a htm_sc struct.

    :param latitude: latitude of the new struct
    :param longitude: longitude of the new struct
    :returns: tuple containing the htm_errcode and htm_sc struct
    """
    cdef htm_sc out
    cdef htm_errcode err_code = htm_sc_init(&out, longitude, latitude)

    return (err_code, out)


def htm_sc_init_wrapped(latitude: float, longitude: float) -> SphericalCoordinate:
    """
    Wraps htm_sc_init, instantiates a wrapped htm_sc struct with given latitude and longitude.

    :param latitude: latitude of the new struct
    :param longitude: longitude of the new struct
    :returns: wrapped htm_sc struct as SphericalCoordinate object
    :raises valueError: if struct instantiation failed
    """
    ec, sc = htm_sc_init_raw(latitude=latitude, longitude=longitude)
    if Errorcode(ec) != Errorcode.HTM_OK:
        raise ValueError(f"htm_sc instantiation failed: {ec}")
    return SphericalCoordinate.from_htm_sc(sc)


def htm_sc_angsep_raw(sc1: htm_sc, sc2: htm_sc) -> float:
    """
    Determine the angle difference between the two given spherical coordinates.

    :param sc1: first position
    :param sc2: second position
    :returns: angle between sc1 and sc2
    """
    return htm_sc_angsep(&sc1, &sc2)


def htm_v3_init_raw(x: float, y: float, z: float) -> tuple[htm_errcode, htm_v3]:
    """
    Wraps htm_v3_init, instantiates a htm_v3 struct.

    :param x: x (first) value of the new struct
    :param y: y (second) value of the new struct
    :param z: z (third) value of the new struct
    :returns: tuple containing the htm_errcode and htm_v3 struct
    """
    cdef htm_v3 out
    cdef htm_errcode err_code = htm_v3_init(&out, x, y, z)

    return (err_code, out)


def htm_v3_init_wrapped(x: float, y: float, z: float) -> V3:
    """
    Wraps htm_v3_init, instantiates a wrapped htm_v3 struct with given x,y,z.

    :param x: x (first) value of the new struct
    :param y: y (second) value of the new struct
    :param z: z (third) value of the new struct
    :returns: tuple containing the wrapped error code and wrapped htm_v3 struct
    :raises valueError: if struct instantiation failed
    """
    ec, v3 = htm_v3_init_raw(x, y, z)
    if Errorcode(ec) != Errorcode.HTM_OK:
        raise ValueError(f"htm_v3 instantiation failed: {ec}")
    return V3.from_htm_v3(v3)


def htm_sc_to_v3_raw(sc: htm_sc) -> tuple[htm_errcode, htm_v3]:
    """
    Wraps htm_sc_tov3, transforms a htm_sc struct into a htm_v3 struct.

    :param sc: htm_sc struct with latitude and longitude
    :returns: tuple containing the htm_errorcode and htm_v3 struct
    """
    cdef htm_v3 out
    cdef htm_errcode err_code = htm_sc_tov3(&out, &sc)

    return (err_code, out)


def htm_v3_to_sc_raw(v3: htm_v3) -> tuple[htm_errcode, htm_sc]:
    """
    Wraps htm_v3_tosc, transforms a htm_v3 struct into a htm_sc struct.

    :param v3: htm_v3 struct with x,y,z
    :returns: tuple containing the htm_errorcode and htm_sc struct
    """
    cdef htm_sc out
    cdef htm_errcode err_code = htm_v3_tosc(&out, &v3)

    return(err_code, out)


def htm_v3_add_raw(v1: htm_v3, v2: htm_v3) -> htm_v3:
    """
    Adds two vectors.

    :param v1: first vector
    :param v2: second vector
    :returns: sum of v1 and v2
    """
    cdef htm_v3 out
    htm_v3_add(&out, &v1, &v2)
    return out


def htm_v3_sub_raw(v1: htm_v3, v2: htm_v3) -> htm_v3:
    """
    Subtracts two vectors.

    :param v1: first vector
    :param v2: second vector
    :returns:  v1 - v2
    """
    cdef htm_v3 out
    htm_v3_sub(&out, &v1, &v2)
    return out


def htm_v3_neg_raw(v1: htm_v3) -> htm_v3:
    """
    Negates the given vector.

    :param v1: first vector
    :returns:  v1 - v2
    """
    cdef htm_v3 out
    htm_v3_neg(&out, &v1)
    return out


def htm_v3_mul_raw(v1: htm_v3, scalar: float) -> htm_v3:
    """
    Scalar vector multiplication.

    :param v1: first vector
    :param scalar: scalar multiplier
    :returns:  v1 * scalar
    """
    cdef htm_v3 out
    htm_v3_mul(&out, &v1, scalar)
    return out


def htm_v3_div_raw(v1: htm_v3, scalar: float) -> htm_v3:
    """
    Scalar vector division.

    :param v1: first vector
    :param scalar: scalar divisor
    :returns:  v1 / divisor
    """
    if scalar == 0:
        raise ValueError(f"Cannot divide by {scalar}")

    cdef htm_v3 out
    htm_v3_div(&out, &v1, scalar)
    return out


cdef extern from "libtinyhtm/src/tinyhtm/htm.h":
    struct htm_tri:
        htm_v3[3] verts
        htm_v3 center
        double radius
        int64_t id
        int level

    int64_t htm_v3_id(const htm_v3 *point, int level)

    htm_errcode htm_tri_init(htm_tri *tri, int64_t id)

    int htm_level(int64_t id)

    int64_t htm_idtodec(int64_t id)


class Triangle():

    @property
    def vertices(self) -> V3[3]:
        """Vertices making up this triangle."""
        return self._vertices

    @property
    def center(self) -> V3:
        """Center point of this triangle."""
        return self._center

    @property
    def radius(self) -> float:
        """Radius of the circle given by the three corners of the triangle."""
        return self._radius

    @property
    def id(self) -> int64_t:
        """HTM ID of this triangle."""
        return self._id

    @property
    def level(self) -> int:
        """Level at which this triangle is within the htm."""
        return self._level

    def __init__(self, vertices: V3[3], center: V3, radius: float, id: int, level: int) -> None:
        """
        Instantiates a triangle and with the given parameters.

        :param vertices: vertices of the triangle
        :param center: center of the triangle
        :param radius: radius of the circle defined by the three vertices
        :param id: htm id of the triangle
        :param level: level at which the triangle is within the htm
        """
        self._vertices = vertices
        self._center = center
        self._radius = radius
        self._id = id
        self._level = level

    def __repr__(self):
        """Detailed representation of this Triangle."""
        return f"Triangle({str(self.__dict__)})"

    def from_htm_tri(struct: htm_tri) -> Triangle:
        """
        Instantiates a triangle based on a htm_tri struct.

        :param struct: struct describing the triangle
        """

        vertices = [V3.from_htm_v3(vertex) for vertex in struct.get("verts")]
        center = V3.from_htm_v3(struct.get("center"))
        radius = struct.get("radius")
        id = struct.get("id")
        level = int(struct.get("level"))

        return Triangle(vertices, center, radius, id, level)

    def from_id(id: int64_t) -> Triangle:
        """
        Instantiates a Triangle object from a given htm id.

        :param id: triangle id
        :returns: triangle object
        """
        return htm_tri_init_wrapped(id)


def htm_v3_id_raw(v: htm_v3, level: int) -> int64_t:
    """
    Retrieves the trixel is for a given v3.

    :param v: v3 vector
    :param level: trixel depth
    :returns: id of the trixel in which v3 lands at the given level
    """
    return htm_v3_id(&v, level)


def htm_tri_init_raw(id: int64_t) -> tuple[htm_errcode, htm_tri]:
    """
    Instantiate a htm_tri struct for a given triangle id.

    :param id: Id of the triangle
    """
    cdef htm_tri triangle
    cdef err_code = htm_tri_init(&triangle, id)

    return (err_code, triangle)


def htm_tri_init_wrapped(id: int64_t) -> Triangle:
    """
    Instantiate a Triangle object for a given triangle id.

    :param id: id of the triangle
    """
    cdef htm_tri triangle
    ec = htm_tri_init(&triangle, id)

    if Errorcode(ec) == Errorcode.HTM_EID:
        raise ValueError(f"Invalid id: {id}")

    if Errorcode(ec) != Errorcode.HTM_OK:
        raise ValueError(f"htm_tri instantiation failed: {ec}")

    return Triangle.from_htm_tri(triangle)


class HTM():

    def get_level(id: int64_t) -> int:
        """
        Retrieves the level of a given ID.

        :param: htm id
        :returns: level of the id
        :raises valueError: if the provided id is invalid
        """
        return htm_level_raw(id)

    def id_to_dec(id: int64_t) -> int64_t:
        """
        Retrieves the decimal representation of an id.

        :param id: triangle id
        :returns: decimal id representation (concatenated [0-3]*)
        """
        return htm_id_to_dec(id)

    def parent(id: int64_t) -> int64_t:
        """
        Determines the parent id of the triangle identified by id.

        :param id: target triangle
        :returns: parent triangle id
        :raises valueError: if the provided id is invalid or the triangle is a root triangle
        """
        # Assert valid id and not root
        if HTM.get_level(id) >= 1:
            return id >> 2

        raise ValueError(f"Root triangle {id} does not have parent!")

    def children(id: int64_t) -> list[int64_t]:
        """
        Gets the children contained in the triangle identified by id.

        :param id: target triangle
        :returns: list of 4 children
        :raises valueError: if the provided id is invalid
        """

        # Assert valid id provided
        HTM.get_level(id)

        children = []
        for i in range(0, 4):
            children.append(id<<2 | i)

        return children


def htm_level_raw(id: int64_t) -> int:
    """
    Retrieves the level of a given ID.

    :param: htm id
    :returns: level of the id
    :raises valueError: if the provided id is invalid
    """
    level = htm_level(id)

    if level < 0:
        raise ValueError(f"Invalid id: {id}")

    return level


def htm_id_to_dec(id: int64_t) -> int64_t:
    """
    Retrieves the decimal representation of an id.

    :param id: triangle id
    :returns: decimal id representation (concatenated [0-3]*)
    """
    return htm_idtodec(id)
