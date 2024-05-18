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

    htm_errcode htm_sc_init(htm_sc *out, double lon_deg, double lat_deg)


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


def htm_sc_init_raw(latitude: float, longitude: float) -> tuple[htm_errcode, htm_sc]:
    """
    Wraps htm_sc_init, instantes a htm_sc struct

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
