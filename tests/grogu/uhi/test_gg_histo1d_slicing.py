from babyyoda.histo1D import Histo1D
import babyyoda.grogu as yoda
from babyyoda.test import assert_equal_histo1d
from babyyoda.util import loc, overflow, underflow


def get_histo1d():
    h = yoda.Histo1D(10, 0, 10, title="test")
    for i in range(12):
        for _ in range(i):
            h.fill(i)
    h.underflow().fill(-1)
    h.overflow().fill(10)
    return Histo1D(h)


def test_slicing_everything():
    yuhi1d = get_histo1d()
    assert yuhi1d.clone() != yuhi1d
    assert_equal_histo1d(yuhi1d.clone(), yuhi1d)
    assert yuhi1d[:] != yuhi1d
    assert_equal_histo1d(yuhi1d[:], yuhi1d)
    assert yuhi1d.clone()[:] != yuhi1d


def test_slicing_subset():
    yuhi1d = get_histo1d()
    assert yuhi1d.clone()[1:3] != yuhi1d
    assert yuhi1d[1:3] != yuhi1d[1:3]
    assert_equal_histo1d(yuhi1d[1:3], yuhi1d[1:3])
    assert yuhi1d[1:3][0].sumW() == yuhi1d[1].sumW()


def test_slicing_upper_bound():
    yuhi1d = get_histo1d()
    print(yuhi1d[: loc(5)])
    assert yuhi1d[: loc(5)][-1].sumW() == yuhi1d[loc(4)].sumW()
    assert yuhi1d[: loc(5)][-1].sumW() == yuhi1d[4].sumW()


def test_slicing_lower_bound():
    yuhi1d = get_histo1d()
    assert yuhi1d[loc(5) :][0].sumW() == yuhi1d[5].sumW()


def test_slicing_mixed_bound():
    yuhi1d = get_histo1d()
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


def test_slicing_overflow():
    yuhi1d = get_histo1d()
    assert (yuhi1d)[overflow].sumW() == yuhi1d[overflow].sumW()
    assert (yuhi1d[:3])[overflow].sumW() == yuhi1d[:3][overflow].sumW()
    assert (yuhi1d)[overflow].sumW() != yuhi1d[:3][overflow].sumW()
    assert (yuhi1d)[overflow].sumW() == yuhi1d[3:][overflow].sumW()
    assert (yuhi1d[:3])[2:][overflow].sumW() == yuhi1d[:3][overflow].sumW()


def test_slicing_underflow():
    yuhi1d = get_histo1d()
    assert (yuhi1d)[underflow].sumW() == yuhi1d[underflow].sumW()
    assert (yuhi1d[3:])[underflow].sumW() == yuhi1d[3:][underflow].sumW()
    assert (yuhi1d)[underflow].sumW() == yuhi1d[:3][underflow].sumW()
    assert (yuhi1d)[underflow].sumW() != yuhi1d[3:][underflow].sumW()
    assert (yuhi1d[3:])[:2][underflow].sumW() == yuhi1d[3:][underflow].sumW()
