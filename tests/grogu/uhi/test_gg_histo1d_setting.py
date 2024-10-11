from babyyoda.histo1D import Histo1D
import babyyoda.grogu as yoda
from babyyoda.util import loc, overflow, underflow


def get_histo1d():
    h = yoda.Histo1D(10, 0, 10, title="test")
    for i in range(12):
        for _ in range(i):
            h.fill(i)
    h.underflow().fill(-1)
    h.overflow().fill(10)
    return Histo1D(h)


def test_setting_index():
    yuhi1d = get_histo1d()
    yuhi1d[1] = yuhi1d[2]
    yuhi1d[7] = yuhi1d[8]
    yuhi1d[3] = yuhi1d[5]
    assert yuhi1d[1].sumW() == yuhi1d[2].sumW()
    assert yuhi1d[7].sumW2() == yuhi1d[8].sumW2()
    assert yuhi1d[3].numEntries() == yuhi1d[5].numEntries()


def test_setting_loc():
    yuhi1d = get_histo1d()
    yuhi1d[loc(1)] = yuhi1d[2]
    yuhi1d[loc(7)] = yuhi1d[8]
    yuhi1d[loc(3)] = yuhi1d[5]
    assert yuhi1d[1].sumW() == yuhi1d[2].sumW()
    assert yuhi1d[7].sumW2() == yuhi1d[8].sumW2()
    assert yuhi1d[3].numEntries() == yuhi1d[5].numEntries()


def test_setting_underflow():
    yuhi1d = get_histo1d()
    yuhi1d[underflow] = yuhi1d[overflow]
    assert yuhi1d[underflow].sumW() == yuhi1d[overflow].sumW()
    assert yuhi1d[underflow].sumW2() == yuhi1d[overflow].sumW2()
    assert yuhi1d[underflow].numEntries() == yuhi1d[overflow].numEntries()


def test_setting_overflow():
    yuhi1d = get_histo1d()
    yuhi1d[overflow] = yuhi1d[1]
    assert yuhi1d[overflow].sumW() == yuhi1d[1].sumW()
    assert yuhi1d[overflow].sumW2() == yuhi1d[1].sumW2()
    assert yuhi1d[overflow].numEntries() == yuhi1d[1].numEntries()
