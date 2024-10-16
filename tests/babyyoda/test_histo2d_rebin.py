import pytest

from babyyoda import grogu
from babyyoda.test import assert_histo2d

# YODA1 does not support histo2d overflows
pytest.importorskip("yoda", minversion="2.0.0")

try:
    from babyyoda import yoda

    yoda_available = True
    # version dependence possible here
except ImportError:
    import babyyoda.grogu as yoda

    yoda_available = False


# TODO use metafunction fixtures instead fo many pytest.mark


def create_histo(backend):
    h = backend(10, 0, 10, 20, 0, 20, title="test")
    w = 0
    for i in range(-10, 22):
        for j in range(-10, 22):
            w += 1
            h.fill(i, j, w)
    # do we already want to use HISTO1D here?
    return h


@pytest.mark.parametrize(
    "factory1", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
def test_histos_rebinXBy(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)

    h1.rebinXBy(2)
    h2.rebinXBy(2)

    assert_histo2d(h1, h2, includeFlow=False)


@pytest.mark.parametrize(
    "factory1", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
def test_histos_rebinXByRange(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)
    h1.rebinXBy(3, 5, 11)
    h2.rebinXBy(3, 5, 11)

    assert_histo2d(h1, h2, includeFlow=False)


@pytest.mark.parametrize(
    "factory1", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
def test_histos_rebinYBy(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)

    h1.rebinYBy(3)
    h2.rebinYBy(3)

    assert_histo2d(h1, h2, includeFlow=False)


@pytest.mark.parametrize(
    "factory1", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Histo2D, grogu.Histo2D_v2, grogu.Histo2D_v3, yoda.Histo2D]
)
def test_histos_rebinYByRange(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)
    h1.rebinYBy(3, 5, 11)
    h2.rebinYBy(3, 5, 11)

    assert_histo2d(h1, h2, includeFlow=False)

    #
    # Flow section
    #


@pytest.mark.parametrize("factory1", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
@pytest.mark.parametrize("factory2", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
def test_histos_rebinYByFlow(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)

    h1.rebinYBy(2)
    h2.rebinYBy(2)

    assert_histo2d(h1, h2, includeFlow=True)


@pytest.mark.parametrize("factory1", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
@pytest.mark.parametrize("factory2", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
def test_histos_rebinYByRangeFlow(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)
    h1.rebinYBy(3, 5, 11)
    h2.rebinYBy(3, 5, 11)

    assert_histo2d(h1, h2, includeFlow=True)


@pytest.mark.parametrize("factory1", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
@pytest.mark.parametrize("factory2", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
def test_histos_rebinXByFlow(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)

    h1.rebinXBy(4)
    h2.rebinXBy(4)

    assert_histo2d(h1, h2, includeFlow=True)


@pytest.mark.parametrize("factory1", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
@pytest.mark.parametrize("factory2", [grogu.Histo2D, grogu.Histo2D_v3, yoda.Histo2D])
def test_histos_rebinXByRangeFlow(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)
    h1.rebinXBy(3, 5, 7)
    h2.rebinXBy(3, 5, 7)

    assert_histo2d(h1, h2, includeFlow=True)
