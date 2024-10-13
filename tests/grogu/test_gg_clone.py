import babyyoda.grogu as yoda
from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT


def test_gg_clone_hist1d_v2():
    h1 = next(iter(yoda.read("tests/test_histo1d_v2.yoda").values()))
    h2 = h1.clone()
    assert GROGU_ANALYSIS_OBJECT.__eq__(h1, h2)
    assert h1 == h2


def test_gg_clone_hist1d_v3():
    h1 = next(iter(yoda.read("tests/test_histo1d_v3.yoda").values()))
    h2 = h1.clone()
    assert GROGU_ANALYSIS_OBJECT.__eq__(h1, h2)
    assert h1 == h2


def test_gg_clone_hist2d_v2():
    h1 = next(iter(yoda.read("tests/test_histo2d_v2.yoda").values()))
    h2 = h1.clone()
    assert GROGU_ANALYSIS_OBJECT.__eq__(h1, h2)
    assert h1 == h2


def test_gg_clone_hist2d_v3():
    h1 = next(iter(yoda.read("tests/test_histo2d_v3.yoda").values()))
    h2 = h1.clone()
    assert GROGU_ANALYSIS_OBJECT.__eq__(h1, h2)
    assert h1 == h2
