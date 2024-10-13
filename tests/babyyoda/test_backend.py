import pytest

from babyyoda import grogu
from babyyoda.test import assert_histo1d

try:
    from babyyoda import yoda

    yoda_available = True
    # version dependence possible here
except ImportError:
    import babyyoda.grogu as yoda

    yoda_available = False

# TODO use metafunction fixtures instead fo many pytest.mark


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
        # babyyoda.Histo1D,
        grogu.Histo1D,
        grogu.Histo1D_v2,
        grogu.Histo1D_v3,
        yoda.Histo1D,
    ],
)
def test_histo1d_backends(factory1, factory2):
    h = create_histo(factory1)
    g = create_histo(factory2)
    assert_histo1d(h, g)
    assert_histo1d(h.to_grogu_v2(), g)
    assert_histo1d(h, g.to_grogu_v2())
    assert_histo1d(h.to_grogu_v2(), g.to_grogu_v2())
    assert_histo1d(h.to_grogu_v3(), g)
    assert_histo1d(h, g.to_grogu_v3())
    assert_histo1d(h.to_grogu_v3(), g.to_grogu_v3())
    assert_histo1d(h.to_grogu_v2(), g.to_grogu_v3())
    # TODO add to_yoda when available
