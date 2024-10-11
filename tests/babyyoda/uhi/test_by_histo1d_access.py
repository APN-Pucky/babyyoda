import pytest
from babyyoda.histo1D import Histo1D
from babyyoda.test import assert_value1d

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
        # babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
@pytest.mark.parametrize(
    "factory2",
    [
        None,
        # babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_access_index(factory1, factory2):
    h = create_histo(factory1)
    g = create_histo(factory2)
    i = 2
    assert_value1d(g[i], h[i])


@pytest.mark.parametrize(
    "factory1",
    [
        None,
        # babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
@pytest.mark.parametrize(
    "factory2",
    [
        None,
        # babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_access_loc(factory1, factory2):
    h = create_histo(factory1)
    g = create_histo(factory2)
    x = 5

    assert_value1d(g[loc(x)], h[loc(x)])
    assert_value1d(g[loc(x)], g[5])
    assert_value1d(h[loc(x)], h[5])


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
@pytest.mark.parametrize(
    "factory2",
    [
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_access_loc_offset(factory1, factory2):
    h = create_histo(factory1)
    g = create_histo(factory2)
    x = 5

    assert_value1d(g[loc(x) + 1], h[loc(x) + 1])
    assert_value1d(g[loc(x) + 1], g[6])


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
@pytest.mark.parametrize(
    "factory2",
    [
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_access_overflow(factory1, factory2):
    h = create_histo(factory1)
    g = create_histo(factory2)

    assert_value1d(g[overflow], h[overflow])


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
@pytest.mark.parametrize(
    "factory2",
    [
        None,
        babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_access_underflow(factory1, factory2):
    h = create_histo(factory1)
    g = create_histo(factory2)

    assert_value1d(g[underflow], h[underflow])
