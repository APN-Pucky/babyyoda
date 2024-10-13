import pytest

import babyyoda
import babyyoda.read
from babyyoda import grogu

try:
    from babyyoda import yoda

    yoda_available = True
    # version dependence possible here
except ImportError:
    import babyyoda.grogu as yoda

    yoda_available = False


@pytest.mark.parametrize(
    "mod",
    [
        babyyoda.read,
        grogu.read,
        yoda.read,
    ],
)
def test_read_histo1d_v2(mod):
    hists = mod("tests/test_histo1d_v2.yoda")
    assert len(hists) == 1


@pytest.mark.parametrize(
    "mod",
    [
        babyyoda.read,
        grogu.read,
        yoda.read,
    ],
)
def test_read_histo1d_v3(mod):
    hists = mod("tests/test_histo1d_v3.yoda")
    assert len(hists) == 1


@pytest.mark.parametrize(
    "mod",
    [
        babyyoda.read,
        grogu.read,
        yoda.read,
    ],
)
def test_read_histo2d_v2(mod):
    hists = mod("tests/test_histo2d_v2.yoda")
    assert len(hists) == 1


@pytest.mark.parametrize(
    "mod",
    [
        babyyoda.read,
        grogu.read,
        yoda.read,
    ],
)
def test_read_histo2d_v3(mod):
    hists = mod("tests/test_histo2d_v3.yoda")
    assert len(hists) == 1
