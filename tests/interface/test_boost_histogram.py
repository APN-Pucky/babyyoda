import random

import pytest

import babyyoda
import babyyoda.read
from babyyoda import grogu
from babyyoda.test import init_yoda

yoda, yoda_available, yoda2 = init_yoda()


@pytest.mark.parametrize(
    "mod",
    [
        babyyoda.read,
        grogu.read,
        yoda.read,
    ],
)
def test_boost_histogram_histo1d_v2(mod):
    hists = mod("tests/test_histo1d_v2.yoda")
    for _, v in hists.items():
        assert isinstance(v, babyyoda.histo1d.UHIHisto1D)
        v.to_boost_histogram()


@pytest.mark.parametrize(
    "mod",
    [
        babyyoda.read,
        grogu.read,
        yoda.read,
    ],
)
@pytest.mark.skipif(not yoda2, reason="yoda >= 2.0.0 is required")
def test_boost_histogram_histo1d_v3(mod):
    hists = mod("tests/test_histo1d_v3.yoda")
    for _, v in hists.items():
        assert isinstance(v, babyyoda.histo1d.UHIHisto1D)
        v.to_boost_histogram()


@pytest.mark.parametrize(
    "mod",
    [
        babyyoda.read,
        grogu.read,
        yoda.read,
    ],
)
def test_boost_histogram_histo2d_v2(mod):
    hists = mod("tests/test_histo2d_v2.yoda")
    for _, v in hists.items():
        assert isinstance(v, babyyoda.histo2d.UHIHisto2D)
        h = v.to_boost_histogram()
        # takes too long to test all bins
        for i in random.sample(range(len(v.xEdges()) - 1), 5):
            for j in random.sample(range(len(v.yEdges()) - 1), 5):
                assert h[i, j].value == v[i, j].sumW()
                assert h[i, j].variance == v[i, j].sumW2()


@pytest.mark.parametrize(
    "mod",
    [
        babyyoda.read,
        grogu.read,
        yoda.read,
    ],
)
@pytest.mark.skipif(not yoda2, reason="yoda >= 2.0.0 is required")
def test_boost_histogram_histo2d_v3(mod):
    hists = mod("tests/test_histo2d_v3.yoda")
    for _, v in hists.items():
        assert isinstance(v, babyyoda.histo2d.UHIHisto2D)
        h = v.to_boost_histogram()
        for i in range(len(v.xEdges()) - 1):
            for j in range(len(v.yEdges()) - 1):
                assert h[i, j].value == v[i, j].sumW()
                assert h[i, j].variance == v[i, j].sumW2()


if __name__ == "main":
    test_boost_histogram_histo1d_v2()
    test_boost_histogram_histo1d_v3()
    test_boost_histogram_histo2d_v2()
    test_boost_histogram_histo2d_v3()
