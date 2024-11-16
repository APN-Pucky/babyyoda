import pytest

from babyyoda import grogu
from babyyoda.util import loc, overflow, underflow

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
    h = backend(10, 0, 10, title="test")
    for i in range(12):
        for _ in range(i):
            h.fill(i)
    # do we already want to use HISTO1D here?
    h.underflow().fill(-1)
    h.overflow().fill(10)

    return h


@pytest.mark.parametrize(
    "factory1",
    [
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_setting_index(factory1):
    yuhi1d = create_histo(factory1)
    yuhi1d[1] = yuhi1d[2]
    yuhi1d[7] = yuhi1d[8]
    yuhi1d[3] = yuhi1d[5]
    assert yuhi1d[1].sumW() == yuhi1d[2].sumW()
    assert yuhi1d[7].sumW2() == yuhi1d[8].sumW2()
    assert yuhi1d[3].numEntries() == yuhi1d[5].numEntries()


@pytest.mark.parametrize(
    "factory1",
    [
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_setting_tuple(factory1):
    yuhi1d = create_histo(factory1)
    yuhi1d[1] = (10.0, [2.0, 4.0], [8.0, 16.0])
    assert yuhi1d[1].numEntries() == 10.0
    assert yuhi1d[1].sumW() == 2.0
    assert yuhi1d[1].sumWX() == 4.0
    assert yuhi1d[1].sumW2() == 8.0
    assert yuhi1d[1].sumWX2() == 16.0


@pytest.mark.parametrize(
    "factory1",
    [
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_setting_loc(factory1):
    yuhi1d = create_histo(factory1)
    yuhi1d[loc(1)] = yuhi1d[2]
    yuhi1d[loc(7)] = yuhi1d[8]
    yuhi1d[loc(3)] = yuhi1d[5]
    assert yuhi1d[1].sumW() == yuhi1d[2].sumW()
    assert yuhi1d[7].sumW2() == yuhi1d[8].sumW2()
    assert yuhi1d[3].numEntries() == yuhi1d[5].numEntries()


@pytest.mark.parametrize(
    "factory1",
    [
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_setting_underflow(factory1):
    yuhi1d = create_histo(factory1)
    yuhi1d[underflow] = yuhi1d[overflow]
    assert yuhi1d[underflow].sumW() == yuhi1d[overflow].sumW()
    assert yuhi1d[underflow].sumW2() == yuhi1d[overflow].sumW2()
    assert yuhi1d[underflow].numEntries() == yuhi1d[overflow].numEntries()


@pytest.mark.parametrize(
    "factory1",
    [
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_setting_overflow(factory1):
    yuhi1d = create_histo(factory1)
    yuhi1d[overflow] = yuhi1d[1]
    assert yuhi1d[overflow].sumW() == yuhi1d[1].sumW()
    assert yuhi1d[overflow].sumW2() == yuhi1d[1].sumW2()
    assert yuhi1d[overflow].numEntries() == yuhi1d[1].numEntries()
