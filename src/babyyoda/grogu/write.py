from typing import Union

from babyyoda.counter import UHICounter
from babyyoda.grogu.counter_v2 import GROGU_COUNTER_V2
from babyyoda.grogu.counter_v3 import GROGU_COUNTER_V3
from babyyoda.grogu.histo1d_v2 import GROGU_HISTO1D_V2
from babyyoda.grogu.histo1d_v3 import GROGU_HISTO1D_V3
from babyyoda.grogu.histo2d_v2 import GROGU_HISTO2D_V2
from babyyoda.grogu.histo2d_v3 import GROGU_HISTO2D_V3
from babyyoda.histo1d import UHIHisto1D
from babyyoda.histo2d import UHIHisto2D
from babyyoda.util import open_write_file

ggHistograms = Union[
    GROGU_COUNTER_V2,
    GROGU_COUNTER_V3,
    GROGU_HISTO1D_V2,
    GROGU_HISTO1D_V3,
    GROGU_HISTO2D_V2,
    GROGU_HISTO2D_V3,
]
uhiHistograms = Union[UHICounter, UHIHisto1D, UHIHisto2D]
Histograms = Union[uhiHistograms, ggHistograms]


def write(
    histograms: Union[list[Histograms], dict[str, Histograms]], file_path: str, gz=False
) -> None:
    """Write multiple histograms to a file in YODA format."""
    with open_write_file(file_path, gz=gz) as f:
        # if dict loop over values
        if isinstance(histograms, dict):
            histograms = histograms.values()
        for histo in histograms:
            f.write(histo.to_string())
            f.write("\n")
