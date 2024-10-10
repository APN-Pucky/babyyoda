import babyyoda
import babyyoda.read


def test_read_histo1d_v2():
    hists = babyyoda.read("tests/test_histo1d_v2.yoda")
    assert len(hists) == 1
