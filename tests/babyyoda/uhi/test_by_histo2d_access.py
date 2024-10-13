import pytest

from babyyoda import grogu
from babyyoda.test import assert_value2d

try:
    from babyyoda import yoda

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
    "factory1",
    [
        # babyyoda.Histo1D,
        grogu.Histo2D,
        grogu.Histo2D_v2,
        grogu.Histo2D_v3,
        yoda.Histo2D,
    ],
)
@pytest.mark.parametrize(
    "factory2",
    [
        # babyyoda.Histo1D,
        grogu.Histo2D,
        grogu.Histo2D_v2,
        grogu.Histo2D_v3,
        yoda.Histo2D,
    ],
)
def test_access_index(factory1, factory2):
    h = create_histo(factory1)
    g = create_histo(factory2)
    i = 2
    j = 3
    assert_value2d(g[i, j], h[i, j])


# TODO more like in 1d
