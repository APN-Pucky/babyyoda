import pytest
from babyyoda.Histo1D_v2 import HISTO1D_V2
from babyyoda.grogu.histo1d_v2 import GROGU_HISTO1D_V2
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

    return HISTO1D_V2(h), HISTO1D_V2(g)


def assert_bin(gb, yb):
    assert gb.xMin() == yb.xMin()
    assert gb.xMax() == yb.xMax()
    assert_value(gb, yb)


def assert_value(gb, yb):
    assert gb.sumW() == yb.sumW()
    assert gb.sumW2() == yb.sumW2()
    assert gb.sumWX() == yb.sumWX()
    assert gb.sumWX2() == yb.sumWX2()
    assert gb.numEntries() == yb.numEntries()


def test_access_index():
    h, g = create_linear_histo1ds()
    i = 2
    assert g[i] == g.bins()[i]

    assert_bin(g[i], h[i])


def test_access_loc():
    h, g = create_linear_histo1ds()
    x = 5
    assert h[loc(x)].xMax() >= x >= h[loc(x)].xMin()
    assert g[loc(x)].xMax() >= x >= g[loc(x)].xMin()

    assert_bin(g[loc(x)], h[loc(x)])
    assert_bin(g[loc(x)], g[5])
    assert_bin(h[loc(x)], h[5])


def test_access_offset():
    h, g = create_linear_histo1ds()
    x = 5
    assert_bin(g[loc(x) + 1], h[loc(x) + 1])
    assert_bin(g[loc(x) + 1], g[6])


def test_access_overflow():
    h, g = create_linear_histo1ds()
    assert_value(g[overflow], h[overflow])


def test_access_underflow():
    h, g = create_linear_histo1ds()
    assert_value(g[underflow], h[underflow])
