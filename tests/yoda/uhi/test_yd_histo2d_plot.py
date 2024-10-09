import pytest
import babyyoda as by
import uhi.typing.plottable as uhit

pytest.importorskip("yoda")


def load_histos():
    h2 = next(iter(by.read_yoda("tests/test_histo2d_v2.yoda").values()))
    return h2


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
    hep.hist2dplot(h2)
