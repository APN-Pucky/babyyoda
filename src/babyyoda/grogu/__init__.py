from babyyoda.grogu.histo1d_v3 import GROGU_HISTO1D_V3
from babyyoda.grogu.histo2d_v2 import GROGU_HISTO2D_V2
from babyyoda.grogu.histo2d_v3 import GROGU_HISTO2D_V3
from .read import read
from .write import write
from .histo1d_v2 import GROGU_HISTO1D_V2


__all__ = ["read", "write"]


def Histo1D(nbins: int, start: float, end: float, title=None, **kwargs):
    return Histo1D_v2(nbins=nbins, start=start, end=end, title=title, **kwargs)


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


def Histo2D_v2(
    nxbins: int,
    xstart: float,
    xend: float,
    nybins: int,
    ystart: float,
    yend: float,
    title=None,
    **kwargs,
):
    return GROGU_HISTO2D_V2(
        d_bins=[
            GROGU_HISTO2D_V2.Bin(
                d_xmin=xstart + i * (xend - xstart) / nxbins,
                d_xmax=xstart + (i + 1) * (xend - xstart) / nxbins,
                d_ymin=ystart + j * (yend - ystart) / nybins,
                d_ymax=ystart + (j + 1) * (yend - ystart) / nybins,
            )
            for i in range(nxbins)
            for j in range(nybins)
        ],
        d_title=title,
        **kwargs,
    )


def Histo2D_v3(
    nxbins: int,
    xstart: float,
    xend: float,
    nybins: int,
    ystart: float,
    yend: float,
    title=None,
    **kwargs,
):
    return GROGU_HISTO2D_V3(
        d_edges=[
            [xstart + i * (xend - xstart) / nxbins for i in range(nxbins + 1)],
            [ystart + i * (yend - ystart) / nybins for i in range(nybins + 1)],
        ],
        d_bins=[
            GROGU_HISTO2D_V3.Bin()
            for _ in range((nxbins + 2) * (nybins + 2))  # add overflow and underflow
        ],
        d_title=title,
        **kwargs,
    )
