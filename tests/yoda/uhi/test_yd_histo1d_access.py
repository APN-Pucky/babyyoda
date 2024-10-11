import pytest
from babyyoda.histo1D import Histo1D
from babyyoda.grogu.histo1d_v2 import GROGU_HISTO1D_V2
from babyyoda.test import assert_bin1d, assert_value1d
from babyyoda.util import loc, overflow, underflow

pytest.importorskip("yoda")


def create_linear_histo1ds():
    import yoda

    h = yoda.Histo1D(10, 0, 10, title="test")

    g = GROGU_HISTO1D_V2(
        d_title="test",
        d_bins=[
            GROGU_HISTO1D_V2.Bin(d_xmin=hb.xMin(), d_xmax=hb.xMax()) for hb in h.bins()
        ],
        d_underflow=GROGU_HISTO1D_V2.Bin(),
        d_overflow=GROGU_HISTO1D_V2.Bin(),
    )

    for i in range(12):
        for _ in range(i):
            h.fill(i)
            g.fill(i)
    h.fill(-1)
    g.fill(-1)
    h.fill(10)
    g.fill(10)

    return Histo1D(h), Histo1D(g)


def test_access_index():
    h, g = create_linear_histo1ds()
    i = 2
    assert g[i] == g.bins()[i]

    assert_bin1d(g[i], h[i])


def test_access_loc():
    h, g = create_linear_histo1ds()
    x = 5
    assert h[loc(x)].xMax() >= x >= h[loc(x)].xMin()
    assert g[loc(x)].xMax() >= x >= g[loc(x)].xMin()

    assert_bin1d(g[loc(x)], h[loc(x)])
    assert_bin1d(g[loc(x)], g[5])
    assert_bin1d(h[loc(x)], h[5])


def test_access_offset():
    h, g = create_linear_histo1ds()
    x = 5
    assert_bin1d(g[loc(x) + 1], h[loc(x) + 1])
    assert_bin1d(g[loc(x) + 1], g[6])


def test_access_overflow():
    h, g = create_linear_histo1ds()
    assert_value1d(g[overflow], h[overflow])


def test_access_underflow():
    h, g = create_linear_histo1ds()
    assert_value1d(g[underflow], h[underflow])
