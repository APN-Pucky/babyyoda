import pytest

from babyyoda.test import assert_value2d
from babyyoda.util import loc

# YODA1 does not support setting
pytest.importorskip("yoda", minversion="2.0.0")


def get_histo2d():
    from babyyoda import yoda

    h = yoda.Histo2D(10, 0, 10, 10, 0, 10, title="test")
    w = 0
    for i in range(-10, 12):
        for j in range(-10, 12):
            w += 1
            h.fill(i, j, w)
    return h


def test_setting_index():
    yuhi1d = get_histo2d()
    yuhi1d[0, 1] = yuhi1d[2, 0]
    yuhi1d[7, 0] = yuhi1d[0, 8]
    yuhi1d[3, 3] = yuhi1d[5, 5]
    assert_value2d(yuhi1d[0, 1], yuhi1d[2, 0])
    assert yuhi1d[0, 1].sumW() == yuhi1d[2, 0].sumW()
    assert_value2d(yuhi1d[7, 0], yuhi1d[0, 8])
    assert yuhi1d[7, 0].sumW2() == yuhi1d[0, 8].sumW2()
    assert_value2d(yuhi1d[3, 3], yuhi1d[5, 5])
    assert yuhi1d[3, 3].numEntries() == yuhi1d[5, 5].numEntries()


def test_setting_loc():
    yuhi1d = get_histo2d()
    yuhi1d[loc(1), 0] = yuhi1d[2, 0]
    yuhi1d[0, loc(7)] = yuhi1d[0, 8]
    yuhi1d[loc(3), loc(3)] = yuhi1d[5, 5]
    assert_value2d(yuhi1d[1, 0], yuhi1d[2, 0])
    assert yuhi1d[1, 0].sumW() == yuhi1d[2, 0].sumW()
    assert_value2d(yuhi1d[0, 7], yuhi1d[0, 8])
    assert yuhi1d[0, 7].sumW2() == yuhi1d[0, 8].sumW2()
    assert_value2d(yuhi1d[3, 3], yuhi1d[5, 5])
    assert yuhi1d[3, 3].numEntries() == yuhi1d[5, 5].numEntries()
