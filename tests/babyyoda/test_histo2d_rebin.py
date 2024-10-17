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
    h = backend(20, 0, 20, 10, 0, 10, title="test")
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
def test_histos_rebinXY(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)

    hh1 = h1.clone()
    hh1.rebinXTo(hh1.xEdges())
    hh1.rebinYTo(hh1.yEdges())

    hh2 = h2.clone()
    hh2.rebinXTo(hh2.xEdges())
    hh2.rebinYTo(hh2.yEdges())

    assert_histo2d(hh1, h1, includeFlow=False)
    assert_histo2d(hh2, h2, includeFlow=False)
    assert_histo2d(hh1, hh2, includeFlow=False)


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

    assert_histo2d(h1, h2, includeFlow=False)

    # for j in range(len(h2.yEdges()) - 1):
    #    for i in range(len(h1.xEdges()) - 1):
    #        print(h1.bins()[i + j * (len(h1.xEdges()) - 1)].numEntries(), end=" ")
    #    print()

    # print()
    h1.rebinXBy(3, 5, 11)
    h2.rebinXBy(3, 5, 11)

    assert h1.xEdges() == h2.xEdges()
    assert h1.yEdges() == h2.yEdges()

    # print(h1, ":")

    # for j in range(len(h1.yEdges()) - 1):
    #    for i in range(len(h1.xEdges()) - 1):
    #        print(h1.bins()[i + j * (len(h1.xEdges()) - 1)].numEntries(), end=" ")
    #    print()

    # print(h2, ":")

    # for j in range(len(h2.yEdges()) - 1):
    #    for i in range(len(h2.xEdges()) - 1):
    #        print(h2.bins()[i + j * (len(h2.xEdges()) - 1)].numEntries(), end=" ")
    #    print()

    # assert h1.integral(includeOverflows=False) == h2.integral(includeOverflows=False)

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
