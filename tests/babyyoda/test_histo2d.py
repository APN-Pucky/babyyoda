import pytest
from babyyoda.test import assert_histo2d

import babyyoda.grogu as grogu

try:
    import babyyoda.yoda as yoda

    yoda_available = True
    # version dependence possible here
except ImportError:
    import babyyoda.grogu as yoda

    yoda_available = False

# TODO use metafunction fixtures instead fo many pytest.mark


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
    "factory", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
def test_create_histo(factory):
    create_histo(factory)


@pytest.mark.parametrize(
    "factory1", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
def test_histos_equal(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)

    assert_histo2d(h1, h2, includeFlow=False)


@pytest.mark.parametrize("factory1", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
@pytest.mark.parametrize("factory2", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
def test_histos_overflow_equal(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)

    assert_histo2d(h1, h2, includeFlow=False)


# TODO more like in 1d
