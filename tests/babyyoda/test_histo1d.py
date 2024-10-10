import pytest
from babyyoda.Histo1D import HISTO1D
from babyyoda.test import assert_histo1d

import babyyoda.grogu as grogu

try:
    import yoda

    yoda_available = True
    # version dependence possible here
except ImportError:
    import babyyoda.grogu as yoda

    yoda_available = False


def create_histo(factory):
    h = factory(10, 0, 10, title="test")
    for i in range(12):
        for _ in range(i):
            h.fill(i)
    # do we already want to use HISTO1D here?
    h = HISTO1D(h)
    h.underflow().fill(-1)
    h.overflow().fill(10)
    return h


@pytest.mark.parametrize(
    "factory", [grogu.Histo1D, grogu.Histo1D_v2, grogu.Histo1D_v3, yoda.Histo1D]
)
def test_create_histo(factory):
    create_histo(factory)


@pytest.mark.parametrize(
    "factory1", [grogu.Histo1D, grogu.Histo1D_v2, grogu.Histo1D_v3, yoda.Histo1D]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Histo1D, grogu.Histo1D_v2, grogu.Histo1D_v3, yoda.Histo1D]
)
def test_histos_equal(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)

    assert_histo1d(h1, h2)
