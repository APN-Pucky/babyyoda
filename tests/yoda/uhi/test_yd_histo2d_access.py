import pytest
from babyyoda.histo2D import Histo2D
from babyyoda.grogu.histo2d_v2 import GROGU_HISTO2D_V2
from babyyoda.test import assert_bin2d
from babyyoda.util import loc

pytest.importorskip("yoda")


def create_histo2d():
    import yoda as yd

    h = yd.Histo2D(10, 0, 10, 10, 0, 10, title="test")

    g = GROGU_HISTO2D_V2(
        d_title="test",
        d_bins=[
            GROGU_HISTO2D_V2.Bin(
                d_xmin=hb.xMin(), d_xmax=hb.xMax(), d_ymin=hb.yMin(), d_ymax=hb.yMax()
            )
            for hb in h.bins()
        ],
        d_underflow=GROGU_HISTO2D_V2.Bin(),
        d_overflow=GROGU_HISTO2D_V2.Bin(),
    )

    for i in range(12):
        for j in range(12):
            for _ in range(i * j):
                h.fill(i, j)
                g.fill(i, j)
    return Histo2D(h), Histo2D(g)


def test_access_index():
    h, g = create_histo2d()

    assert_bin2d(h[1, 0], h.bin(10))
    assert_bin2d(h[0, 2], h.bin(2))

    assert_bin2d(g[1, 0], g.bin(10))
    assert_bin2d(g[0, 2], g.bin(2))


def test_access_loc():
    h, g = create_histo2d()

    assert_bin2d(h[loc(3), loc(4)], h.binAt(3, 4))
    assert_bin2d(g[loc(3), loc(4)], g.binAt(3, 4))
