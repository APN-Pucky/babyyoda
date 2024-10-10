from babyyoda.grogu.histo1d_v3 import GROGU_HISTO1D_V3
from .read import read
from .write import write
from .histo1d_v2 import GROGU_HISTO1D_V2


__all__ = ["read", "write"]


# TODO same function for Hist1D in babyyoda.Histo1D_v2, but how pick backend? probably just yoda if yoda available
def Histo1D(nbins: int, start: float, end: float, title=None, **kwargs):
    return Histo1D_v2(nbins, start, end, title, **kwargs)


def Histo1D_v2(nbins: int, start: float, end: float, title=None, **kwargs):
    return GROGU_HISTO1D_V2(
        d_bins=[
            GROGU_HISTO1D_V2.Bin(
                d_xmin=start + i * (end - start) / nbins,
                d_xmax=start + (i + 1) * (end - start) / nbins,
            )
            for i in range(nbins)
        ],
        d_overflow=GROGU_HISTO1D_V2.Bin(),
        d_underflow=GROGU_HISTO1D_V2.Bin(),
        d_title=title,
        **kwargs,
    )


def Histo1D_v3(nbins: int, start: float, end: float, title=None, **kwargs):
    return GROGU_HISTO1D_V3(
        d_edges=[start + i * (end - start) / nbins for i in range(nbins + 1)],
        d_bins=[
            GROGU_HISTO1D_V3.Bin()
            for i in range(nbins + 2)  # add overflow and underflow
        ],
        d_title=title,
        **kwargs,
    )
