import warnings

from babyyoda import grogu
from babyyoda.histo1D import Histo1D
from babyyoda.histo2D import Histo2D


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
    import yoda as yd

    ret = {}
    for k, v in yd.read(file_path).items():
        if isinstance(v, yd.Histo1D):
            ret[k] = Histo1D(v)
        elif isinstance(v, yd.Histo2D):
            ret[k] = Histo2D(v)
        else:
            ret[k] = v
    return ret


def read_grogu(file_path: str):
    """
    Wrap grogu histograms in the by HISTO1D_V2 class
    """
    ret = {}
    for k, v in grogu.read(file_path).items():
        if isinstance(v, grogu.histo1d_v2.GROGU_HISTO1D_V2):
            ret[k] = Histo1D(v)
        elif isinstance(v, grogu.histo2d_v2.GROGU_HISTO2D_V2):
            ret[k] = Histo2D(v)
        else:
            ret[k] = v
    return ret
