from typing import Any

from babyyoda.grogu.counter_v2 import Counter_v2
from babyyoda.grogu.counter_v3 import GROGU_COUNTER_V3, Counter_v3
from babyyoda.grogu.histo1d_v2 import Histo1D_v2
from babyyoda.grogu.histo1d_v3 import GROGU_HISTO1D_V3, Histo1D_v3
from babyyoda.grogu.histo2d_v2 import Histo2D_v2
from babyyoda.grogu.histo2d_v3 import GROGU_HISTO2D_V3, Histo2D_v3

from .read import read
from .write import write

__all__ = [
    "read",
    "write",
    "Counter_v2",
    "Counter_v3",
    "Histo1D_v2",
    "Histo1D_v3",
    "Histo2D_v2",
    "Histo2D_v3",
]


def Counter(*args: Any, **kwargs: Any) -> GROGU_COUNTER_V3:
    return Counter_v3(*args, **kwargs)


def Histo1D(*args: Any, **kwargs: Any) -> GROGU_HISTO1D_V3:
    return Histo1D_v3(*args, **kwargs)


def Histo2D(
    *args: Any,
    **kwargs: Any,
) -> GROGU_HISTO2D_V3:
    return Histo2D_v3(
        *args,
        **kwargs,
    )
