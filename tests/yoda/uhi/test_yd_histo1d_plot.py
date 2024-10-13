import pytest
import uhi.typing.plottable as uhit

import babyyoda as by

pytest.importorskip("yoda")


def load_histos():
    return next(iter(by.read_yoda("tests/test_histo1d_v2.yoda").values()))


def test_plottable():
    h2 = load_histos()
    assert isinstance(h2, uhit.PlottableHistogram)


def test_plottable_histoprint():
    from histoprint import print_hist

    h2 = load_histos()
    print_hist(h2)


def test_plottable_mplhep():
    import mplhep as hep

    h2 = load_histos()
    hep.histplot(h2)
