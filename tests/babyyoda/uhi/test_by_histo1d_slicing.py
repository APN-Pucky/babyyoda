import pytest
from babyyoda.histo1D import Histo1D
from babyyoda.test import assert_equal_histo1d

import babyyoda
import babyyoda.grogu as grogu
from babyyoda.util import loc, overflow, underflow

try:
    import yoda

    yoda_available = True
    # version dependence possible here
except ImportError:
    import babyyoda.grogu as yoda

    yoda_available = False

# TODO use metafunction fixtures instead fo many pytest.mark


def create_histo(backend):
    h = Histo1D(10, 0, 10, title="test", backend=backend)
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
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_slicing_everything(factory1):
    yuhi1d = create_histo(factory1)
    assert yuhi1d.clone() != yuhi1d
    assert_equal_histo1d(yuhi1d.clone(), yuhi1d)
    assert yuhi1d[:] != yuhi1d
    assert_equal_histo1d(yuhi1d[:], yuhi1d)
    assert yuhi1d.clone()[:] != yuhi1d


@pytest.mark.parametrize(
    "factory1",
    [
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_slicing_subset(factory1):
    yuhi1d = create_histo(factory1)
    assert yuhi1d.clone()[1:3] != yuhi1d
    assert yuhi1d[1:3] != yuhi1d[1:3]
    assert_equal_histo1d(yuhi1d[1:3], yuhi1d[1:3])
    assert yuhi1d[1:3][0].sumW() == yuhi1d[1].sumW()


@pytest.mark.parametrize(
    "factory1",
    [
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_slicing_upper_bound(factory1):
    yuhi1d = create_histo(factory1)
    print(yuhi1d[: loc(5)])
    assert yuhi1d[: loc(5)][-1].sumW() == yuhi1d[loc(4)].sumW()
    assert yuhi1d[: loc(5)][-1].sumW() == yuhi1d[4].sumW()


@pytest.mark.parametrize(
    "factory1",
    [
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_slicing_lower_bound(factory1):
    yuhi1d = create_histo(factory1)
    assert yuhi1d[loc(5) :][0].sumW() == yuhi1d[5].sumW()


@pytest.mark.parametrize(
    "factory1",
    [
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_slicing_mixed_bound(factory1):
    yuhi1d = create_histo(factory1)
    assert yuhi1d[1:9] != yuhi1d[1:-1]
    assert_equal_histo1d(yuhi1d[1:9], yuhi1d[1:-1])
    assert yuhi1d[1:] != yuhi1d[1:10]
    assert_equal_histo1d(yuhi1d[1:], yuhi1d[1:10])
    assert yuhi1d[1:][2:-1] != yuhi1d[1:10][2:8]
    assert_equal_histo1d(yuhi1d[1:][2:-1], yuhi1d[1:10][2:8])
    assert yuhi1d[:3][2:] != yuhi1d[:3][2:]
    assert_equal_histo1d(yuhi1d[:3][2:], yuhi1d[:3][2:])

    assert yuhi1d[:3][overflow].sumW() == yuhi1d[2:3][overflow].sumW()
    assert yuhi1d[:3][2:][overflow].sumW() == yuhi1d[2:3][overflow].sumW()
    assert yuhi1d[2:][:3] != yuhi1d[2:5]
    assert_equal_histo1d(yuhi1d[2:][:3], yuhi1d[2:5])


@pytest.mark.parametrize(
    "factory1",
    [
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_slicing_overflow(factory1):
    yuhi1d = create_histo(factory1)
    assert (yuhi1d)[overflow].sumW() == yuhi1d[overflow].sumW()
    assert (yuhi1d[:3])[overflow].sumW() == yuhi1d[:3][overflow].sumW()
    assert (yuhi1d)[overflow].sumW() != yuhi1d[:3][overflow].sumW()
    assert (yuhi1d)[overflow].sumW() == yuhi1d[3:][overflow].sumW()
    assert (yuhi1d[:3])[2:][overflow].sumW() == yuhi1d[:3][overflow].sumW()


@pytest.mark.parametrize(
    "factory1",
    [
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_slicing_underflow(factory1):
    yuhi1d = create_histo(factory1)
    assert (yuhi1d)[underflow].sumW() == yuhi1d[underflow].sumW()
    assert (yuhi1d[3:])[underflow].sumW() == yuhi1d[3:][underflow].sumW()
    assert (yuhi1d)[underflow].sumW() == yuhi1d[:3][underflow].sumW()
    assert (yuhi1d)[underflow].sumW() != yuhi1d[3:][underflow].sumW()
    assert (yuhi1d[3:])[:2][underflow].sumW() == yuhi1d[3:][underflow].sumW()
