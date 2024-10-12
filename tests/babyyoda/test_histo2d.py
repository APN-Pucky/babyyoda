import pytest
from babyyoda.histo2D import Histo2D
from babyyoda.test import assert_histo2d

import babyyoda.grogu as grogu

try:
    import yoda

    yoda_available = True
    # version dependence possible here
except ImportError:
    import babyyoda.grogu as yoda

    yoda_available = False

# TODO use metafunction fixtures instead fo many pytest.mark


def create_histo(backend):
    h = Histo2D(10, 0, 10, 10, 0, 10, title="test", backend=backend)
    w = 0
    for i in range(-10, 12):
        for j in range(-10, 12):
            w += 1
            h.fill(i, j, w)
    # do we already want to use HISTO1D here?
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

    assert_histo2d(h1, h2)


# TODO more like in 1d
