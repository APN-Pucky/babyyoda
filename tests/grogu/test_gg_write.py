from babyyoda.grogu import read, write


def test_gg_write_histo1d_v2():
    hists = read("tests/test_histo1d_v2.yoda")
    write(hists, "test.yoda")

    with open("test.yoda") as f1, open("tests/test_histo1d_v2.yoda") as f2:
        assert f1.read() == f2.read()


def test_gg_write_histo1d_v3():
    hists = read("tests/test_histo1d_v3.yoda")
    write(hists, "test.yoda")

    with open("test.yoda") as f1, open("tests/test_histo1d_v3.yoda") as f2:
        assert f1.read() == f2.read()


def test_gg_write_histo2d_v2():
    hists = read("tests/test_histo2d_v2.yoda")
    write(hists, "test.yoda")

    with open("test.yoda") as f1, open("tests/test_histo2d_v2.yoda") as f2:
        assert f1.read() == f2.read()


def test_gg_write_histo2d_v3():
    hists = read("tests/test_histo2d_v3.yoda")
    write(hists, "test.yoda")

    with open("test.yoda") as f1, open("tests/test_histo2d_v3.yoda") as f2:
        assert f1.read() == f2.read()
