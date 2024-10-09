import babyyoda as by
import uhi.typing.plottable as uhit


def load_histos():
    g2 = next(iter(by.read_grogu("tests/test2d.yoda").values()))
    h2 = next(iter(by.read_yoda("tests/test2d.yoda").values()))
    return g2, h2


def test_plottable():
    h2, g2 = load_histos()
    assert isinstance(h2, uhit.PlottableHistogram)
    assert isinstance(g2, uhit.PlottableHistogram)


def test_plottable_histoprint():
    from histoprint import print_hist

    h2, g2 = load_histos()
    print_hist(h2)
    print_hist(g2)


def test_plottable_mplhep():
    import mplhep as hep

    h2, g2 = load_histos()
    hep.hist2dplot(h2)
    hep.hist2dplot(g2)
