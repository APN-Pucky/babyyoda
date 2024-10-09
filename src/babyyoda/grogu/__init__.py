from .read import read
from .histo1d_v2 import GROGU_HISTO1D_V2 as Histo1D_v2


__all__ = ["read"]


# TODO same function for Hist1D in babyyoda.Histo1D_v2, but how pick backend? probably just yoda if yoda available
def Histo1D(nbins: int, start: float, end: float, title=None, **kwargs):
    return Histo1D_v2(
        d_bins=[
            Histo1D_v2.Bin(
                d_xmin=start + i * (end - start) / nbins,
                d_xmax=start + (i + 1) * (end - start) / nbins,
            )
            for i in range(nbins)
        ],
        d_overflow=Histo1D_v2.Bin(),
        d_underflow=Histo1D_v2.Bin(),
        d_title=title,
        **kwargs,
    )
