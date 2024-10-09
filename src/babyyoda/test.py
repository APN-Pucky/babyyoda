# TODO maybe promote all these to __eq__


def assert_ao(g, y):
    assert g.name() == y.name()
    assert g.path() == y.path()
    assert g.title() == y.title()
    assert g.type() == y.type()


def assert_bin1d(gb, yb):
    assert gb.xMin() == yb.xMin()
    assert gb.xMax() == yb.xMax()
    assert_value1d(gb, yb)


def assert_value1d(gb, yb):
    assert gb.sumW() == yb.sumW()
    assert gb.sumW2() == yb.sumW2()
    assert gb.sumWX() == yb.sumWX()
    assert gb.sumWX2() == yb.sumWX2()
    assert gb.numEntries() == yb.numEntries()


def assert_histo1d(gh1, yh1):
    assert_ao(gh1, yh1)

    assert len(gh1.bins()) == len(yh1.bins())

    for gb, yb in zip(gh1.bins(), yh1.bins()):
        assert_bin1d(gb, yb)

    assert_value1d(gh1.overflow(), yh1.overflow())
    assert_value1d(gh1.underflow(), gh1.underflow())


def assert_bin2d(gb, yb):
    assert gb.xMin() == yb.xMin()
    assert gb.xMax() == yb.xMax()
    assert gb.yMin() == yb.yMin()
    assert gb.yMax() == yb.yMax()
    assert_value2d(gb, yb)


def assert_value2d(gb, yb):
    assert gb.sumW() == yb.sumW()
    assert gb.sumW2() == yb.sumW2()
    assert gb.sumWX() == yb.sumWX()
    assert gb.sumWX2() == yb.sumWX2()
    assert gb.sumWY() == yb.sumWY()
    assert gb.sumWY2() == yb.sumWY2()
    if hasattr(gb, "crossTerm") and hasattr(yb, "crossTerm"):
        assert gb.crossTerm(0, 1) == yb.crossTerm(0, 1)
    if hasattr(gb, "sumWXY") and hasattr(yb, "sumWXY"):
        assert gb.sumWXY() == yb.sumWXY()
    assert gb.numEntries() == yb.numEntries()


def assert_histo2d(gh1, yh1):
    assert_ao(gh1, yh1)

    assert len(gh1.bins()) == len(yh1.bins())

    for gb, yb in zip(gh1.bins(), yh1.bins()):
        assert_bin1d(gb, yb)
