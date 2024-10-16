from babyyoda.grogu.counter_v2 import Counter_v2
from babyyoda.grogu.counter_v3 import Counter_v3
from babyyoda.grogu.histo1d_v2 import Histo1D_v2
from babyyoda.grogu.histo1d_v3 import Histo1D_v3
from babyyoda.grogu.histo2d_v2 import Histo2D_v2
from babyyoda.grogu.histo2d_v3 import Histo2D_v3

from .read import read
from .write import write

__all__ = [
    "read",
    "write",
    "Counter_v2",
    "Counter_v3",
    "Histo1D_v2",
    "Histo1D_v3",
    "Histo2D_v2",
    "Histo2D_v3",
]


def Counter(*args, **kwargs):
    return Counter_v3(*args, **kwargs)


def Histo1D(*args, **kwargs):
    return Histo1D_v3(*args, **kwargs)


def Histo2D(
    nxbins: int,
    xstart: float,
    xend: float,
    nybins: int,
    ystart: float,
    yend: float,
    title=None,
    **kwargs,
):
    return Histo2D_v3(
        nxbins=nxbins,
        xstart=xstart,
        xend=xend,
        nybins=nybins,
        ystart=ystart,
        yend=yend,
        title=title,
        **kwargs,
    )
