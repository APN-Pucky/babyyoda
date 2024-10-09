import babyyoda as by
import uhi.typing.plottable as uhit


def load_histos():
    g2 = next(iter(by.read_grogu("tests/test_histo1d_v2.yoda").values()))
    return g2


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
