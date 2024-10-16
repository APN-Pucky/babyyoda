import pytest

from babyyoda import grogu
from babyyoda.test import assert_value0d, init_yoda

yoda, yoda_available, yoda2 = init_yoda()


def create_histo(factory):
    h = factory(title="test")
    for i in range(12):
        for _ in range(i):
            h.fill(i)
    return h


@pytest.mark.parametrize(
    "factory", [grogu.Counter, grogu.Counter_v2, grogu.Counter_v3, yoda.Counter]
)
def test_create_histo(factory):
    create_histo(factory)


@pytest.mark.parametrize(
    "factory1", [grogu.Counter, grogu.Counter_v2, grogu.Counter_v3, yoda.Counter]
)
@pytest.mark.parametrize(
    "factory2", [grogu.Counter, grogu.Counter_v2, grogu.Counter_v3, yoda.Counter]
)
def test_histos_equal(factory1, factory2):
    h1 = create_histo(factory1)
    h2 = create_histo(factory2)

    assert_value0d(h1, h2)
