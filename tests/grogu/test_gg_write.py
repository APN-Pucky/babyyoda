from babyyoda.grogu import read
from babyyoda.grogu import write


def test_gg_write_histo1d_v2():
    hists = read("tests/test_histo1d_v2.yoda")
    write(hists, "test.yoda")


def test_gg_write_histo1d_v3():
    hists = read("tests/test_histo1d_v3.yoda")
    write(hists, "test.yoda")


def test_gg_write_histo2d_v2():
    hists = read("tests/test_histo2d_v2.yoda")
    write(hists, "test.yoda")
