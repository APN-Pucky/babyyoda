import pytest

from babyyoda import grogu
from babyyoda.test import assert_histo1d, init_yoda

yoda, yoda_available, yoda2 = init_yoda()


def create_histo(factory):
    h = factory(10, 0, 10, title="test")
    for i in range(12):
        for _ in range(i):
            h.fill(i)
    # do we already want to use HISTO1D here?
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


@pytest.mark.parametrize(
    "factory1", [grogu.Histo1D, grogu.Histo1D_v2, grogu.Histo1D_v3, yoda.Histo1D]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Histo1D, grogu.Histo1D_v2, grogu.Histo1D_v3, yoda.Histo1D]
)
def test_histos_rebinby(factory1, factory2):
    o1 = create_histo(factory1)
    o2 = create_histo(factory2)

    h1 = o1.clone()
    h2 = o2.clone()

    h1.rebinBy(2)
    h2.rebinBy(2)

    # check that modifications happen
    with pytest.raises(AssertionError):
        assert_histo1d(o1, h1)
    with pytest.raises(AssertionError):
        assert_histo1d(o2, h2)

    assert_histo1d(h1, h2)


@pytest.mark.skipif(
    not yoda2, reason="yoda >= 2.0.0 is required, since yoda1 rebins differently"
)
@pytest.mark.parametrize(
    "factory1", [grogu.Histo1D, grogu.Histo1D_v2, grogu.Histo1D_v3, yoda.Histo1D]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Histo1D, grogu.Histo1D_v2, grogu.Histo1D_v3, yoda.Histo1D]
)
def test_histos_rebinby_begin(factory1, factory2):
    o1 = create_histo(factory1)
    o2 = create_histo(factory2)

    h1 = o1.clone()
    h2 = o2.clone()

    h1.rebinBy(2)
    h2.rebinBy(2)

    # check that modifications happen
    with pytest.raises(AssertionError):
        assert_histo1d(o1, h1)
    with pytest.raises(AssertionError):
        assert_histo1d(o2, h2)

    assert_histo1d(h1, h2)

    h1 = o1.clone()
    h2 = o2.clone()

    h1.rebinBy(3, begin=2)
    h2.rebinBy(3, begin=2)

    assert_histo1d(h1, h2)

    h1 = o1.clone()
    h2 = o2.clone()

    h1.rebinBy(3, begin=2, end=7)
    h2.rebinBy(3, begin=2, end=7)

    assert_histo1d(h1, h2)


@pytest.mark.parametrize(
    "factory1", [grogu.Histo1D, grogu.Histo1D_v2, grogu.Histo1D_v3, yoda.Histo1D]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Histo1D, grogu.Histo1D_v2, grogu.Histo1D_v3, yoda.Histo1D]
)
def test_histos_rebinto(factory1, factory2):
    o1 = create_histo(factory1)
    o2 = create_histo(factory2)

    h1 = o1.clone()
    h2 = o2.clone()

    h1.rebinTo([0.0, 1.0, 2.0, 4.0, 5.0, 6.0, 9.0])
    h2.rebinTo([0.0, 1.0, 2.0, 4.0, 5.0, 6.0, 9.0])

    # check that modifications happen
    with pytest.raises(AssertionError):
        assert_histo1d(o1, h1)
    with pytest.raises(AssertionError):
        assert_histo1d(o2, h2)

    assert_histo1d(h1, h2)
