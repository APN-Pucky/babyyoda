import babyyoda
import babyyoda.read


def test_read_histo1d_v2():
    hists = babyyoda.read("tests/test_histo1d_v2.yoda")
    assert len(hists) == 1


def test_read_histo1d_v3():
    hists = babyyoda.read("tests/test_histo1d_v3.yoda")
    assert len(hists) == 1


def test_read_histo2d_v2():
    hists = babyyoda.read("tests/test_histo2d_v2.yoda")
    assert len(hists) == 1


def test_read_histo2d_v3():
    hists = babyyoda.read("tests/test_histo2d_v3.yoda")
    assert len(hists) == 1
