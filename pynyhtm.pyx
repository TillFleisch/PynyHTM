"""Wrapping classes and methods for libtinyhtm."""
from enum import Enum


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

    def get_htm_sc(self):
        """Gets a htm_sc strcut based on this spherical coordinate."""
        return htm_sc(self._latitude, self._longitude)

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

    def to_v3(self) -> tuple[Errorcode, V3]:
        """Transforms this spherical coordinate into a v3 vector."""
        ec, v3 = htm_sc_to_v3_raw(self.get_htm_sc())
        return (Errorcode(ec), V3.from_htm_v3(v3))


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

    def to_sc(self) -> tuple[Errorcode, SphericalCoordinate]:
        """Transforms this V3 vector into a sphercial coordinate."""
        ec, sc = htm_v3_to_sc_raw(self.get_htm_v3())
        return (Errorcode(ec), SphericalCoordinate.from_htm_sc(sc))


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


def htm_sc_init_wrapped(latitude: float, longitude: float) -> tuple[Errorcode, SphericalCoordinate]:
    """
    Wraps htm_sc_init, instantiates a wrapped htm_sc struct with given latitude and longitude.

    :param latitude: latitude of the new struct
    :param longitude: longitude of the new struct
    :returns: tuple containing the wrapped error code and wrapped htm_sc struct
    """
    err_code, sc = htm_sc_init_raw(latitude=latitude, longitude=longitude)
    return (Errorcode(err_code), SphericalCoordinate.from_htm_sc(sc))


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


def htm_v3_init_wrapped(x: float, y: float, z: float) -> tuple[Errorcode, V3]:
    """
    Wraps htm_v3_init, instantiates a wrapped htm_v3 struct with given x,y,z.

    :param x: x (first) value of the new struct
    :param y: y (second) value of the new struct
    :param z: z (third) value of the new struct
    :returns: tuple containing the wrapped error code and wrapped htm_v3 struct
    """
    err_code, v3 = htm_v3_init_raw(x, y, z)
    return (Errorcode(err_code), V3.from_htm_v3(v3))


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
