import pytest

from babyyoda import grogu
from babyyoda.test import assert_value2d
from babyyoda.util import loc

try:
    from babyyoda import yoda

    yoda_available = True
    # version dependence possible here
except ImportError:
    import babyyoda.grogu as yoda

    yoda_available = False

# YODA1 does not support setting
pytest.importorskip("yoda", minversion="2.0.0")


def create_histo(backend):
    h = backend(10, 0, 10, 10, 0, 10, title="test")
    w = 0
    for i in range(-10, 12):
        for j in range(-10, 12):
            w += 1
            h.fill(i, j, w)
    # do we already want to use HISTO1D here?
    return h


@pytest.mark.parametrize(
    "factory1",
    [
        # babyyoda.Histo1D,
        grogu.Histo2D,
        grogu.Histo2D_v2,
        grogu.Histo2D_v3,
        yoda.Histo2D,
    ],
)
def test_setting_index(factory1):
    yuhi1d = create_histo(factory1)
    yuhi1d[0, 1] = yuhi1d[2, 0]
    yuhi1d[7, 0] = yuhi1d[0, 8]
    yuhi1d[3, 3] = yuhi1d[5, 5]
    assert_value2d(yuhi1d[0, 1], yuhi1d[2, 0])
    assert yuhi1d[0, 1].sumW() == yuhi1d[2, 0].sumW()
    assert_value2d(yuhi1d[7, 0], yuhi1d[0, 8])
    assert yuhi1d[7, 0].sumW2() == yuhi1d[0, 8].sumW2()
    assert_value2d(yuhi1d[3, 3], yuhi1d[5, 5])
    assert yuhi1d[3, 3].numEntries() == yuhi1d[5, 5].numEntries()


@pytest.mark.parametrize(
    "factory1",
    [
        # babyyoda.Histo1D,
        grogu.Histo2D,
        grogu.Histo2D_v2,
        grogu.Histo2D_v3,
        yoda.Histo2D,
    ],
)
def test_setting_tuple(factory1):
    yuhi1d = create_histo(factory1)
    yuhi1d[0, 1] = (10.0, [2.0, 4.0, 8.0], [16.0, 32.0, 64.0], [128.0])
    assert yuhi1d[0, 1].numEntries() == 10.0
    assert yuhi1d[0, 1].sumW() == 2.0
    assert yuhi1d[0, 1].sumWX() == 4.0
    assert yuhi1d[0, 1].sumWY() == 8.0
    assert yuhi1d[0, 1].sumW2() == 16.0
    assert yuhi1d[0, 1].sumWX2() == 32.0
    assert yuhi1d[0, 1].sumWY2() == 64.0
    assert yuhi1d[0, 1].crossTerm(0, 1) == 128.0


@pytest.mark.parametrize(
    "factory1",
    [
        # babyyoda.Histo1D,
        grogu.Histo2D,
        grogu.Histo2D_v2,
        grogu.Histo2D_v3,
        yoda.Histo2D,
    ],
)
def test_setting_loc(factory1):
    yuhi1d = create_histo(factory1)
    yuhi1d[loc(1), 0] = yuhi1d[2, 0]
    yuhi1d[0, loc(7)] = yuhi1d[0, 8]
    yuhi1d[loc(3), loc(3)] = yuhi1d[5, 5]
    assert_value2d(yuhi1d[1, 0], yuhi1d[2, 0])
    assert yuhi1d[1, 0].sumW() == yuhi1d[2, 0].sumW()
    assert_value2d(yuhi1d[0, 7], yuhi1d[0, 8])
    assert yuhi1d[0, 7].sumW2() == yuhi1d[0, 8].sumW2()
    assert_value2d(yuhi1d[3, 3], yuhi1d[5, 5])
    assert yuhi1d[3, 3].numEntries() == yuhi1d[5, 5].numEntries()
