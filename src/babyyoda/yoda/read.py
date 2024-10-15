import yoda as yd

from babyyoda.yoda.histo1d import Histo1D
from babyyoda.yoda.histo2d import Histo2D


def read(file_path: str):
    """
    Wrap yoda histograms in the by HISTO1D_V2 class
    """

    ret = {}
    for k, v in yd.read(file_path).items():
        if isinstance(v, yd.Histo1D):
            ret[k] = Histo1D(v)
        elif isinstance(v, yd.Histo2D):
            ret[k] = Histo2D(v)
        else:
            ret[k] = v
    return ret
