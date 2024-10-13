import pytest
import babyyoda
import babyyoda.read
import babyyoda.grogu as grogu
from babyyoda.test import assert_histo1d, assert_histo2d
from babyyoda.util import is_yoda, uses_yoda

try:
    import yoda

    yoda_available = True
    # version dependence possible here
except ImportError:
    import babyyoda.grogu as yoda

    yoda_available = False


def test_is_from_package():
    if yoda_available:
        h = next(iter(yoda.read("tests/test_histo1d_v2.yoda").values()))
        assert uses_yoda(h)
        assert is_yoda(h)
        h = next(iter(babyyoda.read("tests/test_histo1d_v2.yoda").values()))
        assert uses_yoda(h)
        assert not is_yoda(h)


# babyyoda, yoda or grogu
@pytest.mark.parametrize(
    "read, write, reread",
    [
        (yoda.read, yoda.write, yoda.read),
        (babyyoda.read, babyyoda.write, babyyoda.read),
        (babyyoda.read_yoda, babyyoda.write, babyyoda.read_yoda),
        (babyyoda.read_grogu, babyyoda.write_grogu, babyyoda.read_grogu),
        (grogu.read, grogu.write, grogu.read),
        (babyyoda.read_yoda, babyyoda.write_grogu, babyyoda.read_grogu),
        (babyyoda.read_yoda, babyyoda.write_grogu, babyyoda.read_yoda),
        (yoda.read, yoda.write, babyyoda.read),
        (babyyoda.read, babyyoda.write, yoda.read),
    ],
)
@pytest.mark.parametrize(
    "filename",
    [
        "test.yoda",
        "test.yoda.gz",
    ],
)
def test_write_histo1d_v2(read, write, reread, filename):
    hs1 = read("tests/test_histo1d_v2.yoda")
    write(hs1, filename)
    hs2 = reread(filename)

    h1 = next(iter(hs1.values()))
    h2 = next(iter(hs2.values()))
    assert_histo1d(h1, h2)


@pytest.mark.parametrize(
    "read, write, reread",
    [
        (yoda.read, yoda.write, yoda.read),
        (babyyoda.read, babyyoda.write, babyyoda.read),
        (babyyoda.read_yoda, babyyoda.write, babyyoda.read_yoda),
        (babyyoda.read_grogu, babyyoda.write_grogu, babyyoda.read_grogu),
        (grogu.read, grogu.write, grogu.read),
        (babyyoda.read_yoda, babyyoda.write_grogu, babyyoda.read_grogu),
        (babyyoda.read_yoda, babyyoda.write_grogu, babyyoda.read_yoda),
        (yoda.read, yoda.write, babyyoda.read),
        (babyyoda.read, babyyoda.write, yoda.read),
    ],
)
@pytest.mark.parametrize(
    "filename",
    [
        "test.yoda",
        "test.yoda.gz",
    ],
)
def test_write_histo1d_v3(read, write, reread, filename):
    hs1 = read("tests/test_histo1d_v3.yoda")
    write(hs1, filename)
    hs2 = reread(filename)

    h1 = next(iter(hs1.values()))
    h2 = next(iter(hs2.values()))
    assert_histo1d(h1, h2)


@pytest.mark.parametrize(
    "read, write, reread",
    [
        (yoda.read, yoda.write, yoda.read),
        (babyyoda.read, babyyoda.write, babyyoda.read),
        (babyyoda.read_yoda, babyyoda.write, babyyoda.read_yoda),
        (babyyoda.read_grogu, babyyoda.write_grogu, babyyoda.read_grogu),
        (grogu.read, grogu.write, grogu.read),
        (babyyoda.read_yoda, babyyoda.write_grogu, babyyoda.read_grogu),
        (babyyoda.read_yoda, babyyoda.write_grogu, babyyoda.read_yoda),
        (yoda.read, yoda.write, babyyoda.read),
        (babyyoda.read, babyyoda.write, yoda.read),
    ],
)
@pytest.mark.parametrize(
    "filename",
    [
        "test.yoda",
        "test.yoda.gz",
    ],
)
def test_write_histo2d_v2(read, write, reread, filename):
    hs1 = read("tests/test_histo2d_v2.yoda")
    write(hs1, filename)
    hs2 = reread(filename)

    h1 = next(iter(hs1.values()))
    h2 = next(iter(hs2.values()))
    assert_histo2d(h1, h2, includeFlow=False)


@pytest.mark.parametrize(
    "read, write, reread",
    [
        (yoda.read, yoda.write, yoda.read),
        (babyyoda.read, babyyoda.write, babyyoda.read),
        (babyyoda.read_yoda, babyyoda.write, babyyoda.read_yoda),
        (babyyoda.read_grogu, babyyoda.write_grogu, babyyoda.read_grogu),
        (grogu.read, grogu.write, grogu.read),
        (babyyoda.read_yoda, babyyoda.write_grogu, babyyoda.read_grogu),
        (babyyoda.read_yoda, babyyoda.write_grogu, babyyoda.read_yoda),
        (yoda.read, yoda.write, babyyoda.read),
        (babyyoda.read, babyyoda.write, yoda.read),
    ],
)
@pytest.mark.parametrize(
    "filename",
    [
        "test.yoda",
        "test.yoda.gz",
    ],
)
def test_write_histo2d_v3(read, write, reread, filename):
    hs1 = read("tests/test_histo2d_v3.yoda")
    write(hs1, filename)
    hs2 = reread(filename)

    h1 = next(iter(hs1.values()))
    h2 = next(iter(hs2.values()))
    assert_histo2d(h1, h2)
