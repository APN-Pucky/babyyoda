import babyyoda
import babyyoda.read

def test_read():
    hists = babyyoda.read("tests/test1d.yoda")
    assert len(hists) == 1