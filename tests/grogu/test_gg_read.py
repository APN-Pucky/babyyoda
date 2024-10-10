import babyyoda.grogu.read as read


def test_gg_read_histo1d_v2():
    hists = read("tests/test_histo1d_v2.yoda")
    assert len(hists) == 1


def test_gg_read_histo1d_v3():
    hists = read("tests/test_histo1d_v3.yoda")
    assert len(hists) == 1


def test_gg_read_histo2d_v2():
    hists = read("tests/test_histo2d_v2.yoda")
    assert len(hists) == 1
