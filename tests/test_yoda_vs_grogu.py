import babyyoda as by
from babyyoda.grogu.grogu_histo1d_v2 import GROGU_HISTO1D_V2


def assert_histo1d(gh1, yh1):
    assert gh1.name() == yh1.name()
    assert gh1.path() == yh1.path()
    assert gh1.title() == yh1.title()
    assert gh1.type() == yh1.type()

    assert len(gh1.bins()) == len(yh1.bins())

    for gb, yb in zip(gh1.bins(), yh1.bins()):
        assert gb.xMin() == yb.xMin()
        assert gb.xMax() == yb.xMax()
        assert gb.sumW() == yb.sumW()
        assert gb.sumW2() == yb.sumW2()
        assert gb.sumWX() == yb.sumWX()
        assert gb.sumWX2() == yb.sumWX2()
        assert gb.numEntries() == yb.numEntries()

    # TODO test overflow and underflow


def test_ao():
    gh1 = next(iter(by.read_grogu("tests/test1d.yoda").values()))
    yh1 = next(iter(by.read_yoda("tests/test1d.yoda").values()))

    assert gh1.name() == yh1.name()
    assert gh1.path() == yh1.path()
    assert gh1.title() == yh1.title()
    assert gh1.type() == yh1.type()

    gh2 = next(iter(by.read_grogu("tests/test2d.yoda").values()))
    yh2 = next(iter(by.read_yoda("tests/test2d.yoda").values()))

    assert gh2.name() == yh2.name()
    assert gh2.path() == yh2.path()
    assert gh2.title() == yh2.title()
    assert gh2.type() == yh2.type()


def test_histo1():
    gh1 = next(iter(by.read_grogu("tests/test1d.yoda").values()))
    yh1 = next(iter(by.read_yoda("tests/test1d.yoda").values()))

    assert len(gh1.bins()) == len(yh1.bins())

    for gb, yb in zip(gh1.bins(), yh1.bins()):
        assert gb.xMin() == yb.xMin()
        assert gb.xMax() == yb.xMax()
        assert gb.sumW() == yb.sumW()
        assert gb.sumW2() == yb.sumW2()
        assert gb.sumWX() == yb.sumWX()
        assert gb.sumWX2() == yb.sumWX2()
        assert gb.numEntries() == yb.numEntries()

    # TODO test overflow and underflow


def test_histo2():
    gh2 = next(iter(by.read_grogu("tests/test2d.yoda").values()))
    yh2 = next(iter(by.read_yoda("tests/test2d.yoda").values()))

    assert len(gh2.bins()) == len(yh2.bins())

    for gb, yb in zip(gh2.bins(), yh2.bins()):
        assert gb.xMin() == yb.xMin()
        assert gb.xMax() == yb.xMax()
        assert gb.yMin() == yb.yMin()
        assert gb.yMax() == yb.yMax()

        assert gb.sumW() == yb.sumW()
        assert gb.sumW2() == yb.sumW2()
        assert gb.numEntries() == yb.numEntries()

    # TODO test overflow and underflow


def test_create_histo1d():
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

    assert_histo1d(g, h)
