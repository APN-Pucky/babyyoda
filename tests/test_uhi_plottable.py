import babyyoda as by

import uhi.typing.plottable as uhit


def load_histos():
    g1 = next(iter(by.read_grogu("tests/test1d.yoda").values()))
    h1 = next(iter(by.read_yoda("tests/test1d.yoda").values()))
    g2 = next(iter(by.read_grogu("tests/test2d.yoda").values()))
    h2 = next(iter(by.read_yoda("tests/test2d.yoda").values()))
    return g1, h1, g2, h2


def test_plottable():
    h1, g1, h2, g2 = load_histos()
    assert isinstance(h1, uhit.PlottableHistogram)
    assert isinstance(g1, uhit.PlottableHistogram)
    assert isinstance(h2, uhit.PlottableHistogram)
    assert isinstance(g2, uhit.PlottableHistogram)


def test_plottable_histoprint():
    from histoprint import print_hist

    h1, g1, h2, g2 = load_histos()
    print_hist(h1)
    print_hist(g1)
    print_hist(h2)
    print_hist(g2)


def test_plottable_mplhep():
    import mplhep as hep

    h1, g1, h2, g2 = load_histos()
    hep.histplot(h1)
    hep.histplot(g1)
    hep.hist2dplot(h2)
    hep.hist2dplot(g2)
