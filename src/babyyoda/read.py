import warnings

from babyyoda import grogu
from babyyoda import yoda


def read(file_path: str):
    try:
        return read_yoda(file_path)
    except ImportError:
        warnings.warn(
            "yoda is not installed, falling back to python grogu implementation"
        )
        return read_grogu(file_path)


def read_yoda(file_path: str):
    """
    Wrap yoda histograms in the by HISTO1D_V2 class
    """
    return yoda.read(file_path)


def read_grogu(file_path: str):
    """
    Wrap grogu histograms in the by HISTO1D_V2 class
    """
    return grogu.read(file_path)
