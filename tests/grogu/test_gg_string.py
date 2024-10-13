# TODO test that from_string and to_string are inverses for bins and histograms

import pytest

import babyyoda
from babyyoda.grogu.histo1d_v2 import GROGU_HISTO1D_V2
from babyyoda.grogu.histo1d_v3 import GROGU_HISTO1D_V3
from babyyoda.grogu.histo2d_v2 import GROGU_HISTO2D_V2
from babyyoda.grogu.histo2d_v3 import GROGU_HISTO2D_V3
from babyyoda.test import assert_bin1d, assert_histo1d, assert_histo2d


@pytest.mark.parametrize(
    ("args", "kwargs", "label"),
    [
        ([0, 1, 5, 6, 7, 8, 10], {}, None),
        ([0.0, 1.0, 5.0, 6.0, 7.0, 8.0, 10.0], {}, None),
        (
            [],
            {
                "d_xmin": 0,
                "d_xmax": 1,
                "d_sumw": 5,
                "d_sumw2": 6,
                "d_sumwx": 7,
                "d_sumwx2": 8,
                "d_numentries": 10,
            },
            None,
        ),
        (
            [],
            {
                "d_xmin": 0.0,
                "d_xmax": 1.0,
                "d_sumw": 5.0,
                "d_sumw2": 6.0,
                "d_sumwx": 7.0,
                "d_sumwx2": 8.0,
                "d_numentries": 10,
            },
            None,
        ),
        (
            [],
            {
                "d_xmin": None,
                "d_xmax": None,
                "d_sumw": 5.0,
                "d_sumw2": 6.0,
                "d_sumwx": 7.0,
                "d_sumwx2": 8.0,
                "d_numentries": 10,
            },
            "Overflow",
        ),
        (
            [],
            {
                "d_xmin": None,
                "d_xmax": None,
                "d_sumw": 5.0,
                "d_sumw2": 6.0,
                "d_sumwx": 7.0,
                "d_sumwx2": 8.0,
                "d_numentries": 10,
            },
            "Underflow",
        ),
    ],
)
def test_gg_histo1d_v2_bin_string(args, kwargs, label):
    b1 = GROGU_HISTO1D_V2.Bin(*args, **kwargs)
    s = b1.to_string(label)
    b2 = GROGU_HISTO1D_V2.Bin.from_string(s)
    assert_bin1d(b1, b2)
    assert b1 == b2


def test_gg_histo1d_v2_string():
    h1 = babyyoda.grogu.Histo1D_v2(10, 0, 10, title="test")
    for w, i in enumerate(range(-10, 12)):
        h1.fill(i, w)
    s = h1.to_string()
    print(s)
    h2 = GROGU_HISTO1D_V2.from_string(s)
    assert_histo1d(h1, h2)
    assert h1 == h2


def test_gg_histo1d_v3_string():
    h1 = babyyoda.grogu.Histo1D_v3(10, 0, 10, title="test")
    for w, i in enumerate(range(-10, 12)):
        h1.fill(i, w)
    s = h1.to_string()
    print(s)
    h2 = GROGU_HISTO1D_V3.from_string(s)
    assert_histo1d(h1, h2)
    assert h1 == h2


def test_gg_histo2d_v2_string():
    h1 = babyyoda.grogu.Histo2D_v2(10, 0, 10, 10, 0, 10, title="test")
    w = 0
    for i in range(-10, 12):
        for j in range(-10, 12):
            w += 1
            h1.fill(i, j, w)
    s = h1.to_string()
    print(s)
    h2 = GROGU_HISTO2D_V2.from_string(s)
    assert_histo2d(h1, h2, includeFlow=False)
    assert h1 == h2


def test_gg_histo2d_v3_string():
    h1 = babyyoda.grogu.Histo2D_v3(10, 0, 10, 10, 0, 10, title="test")
    w = 0
    for i in range(-10, 12):
        for j in range(-10, 12):
            w += 1
            h1.fill(i, j, w)
    s = h1.to_string()
    print(s)
    h2 = GROGU_HISTO2D_V3.from_string(s)
    assert_histo2d(h1, h2, includeFlow=True)
    assert h1 == h2
