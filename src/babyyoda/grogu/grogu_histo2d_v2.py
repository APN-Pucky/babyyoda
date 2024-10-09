import re
from dataclasses import dataclass, field
from typing import Optional

from babyyoda.grogu.grogu_analysis_object import GROGU_ANALYSIS_OBJECT


@dataclass
class GROGU_HISTO2D_V2(GROGU_ANALYSIS_OBJECT):
    @dataclass
    class Bin:
        d_xmin: Optional[float] = None
        d_xmax: Optional[float] = None
        d_ymin: Optional[float] = None
        d_ymax: Optional[float] = None
        d_sumw: float = 0.0
        d_sumw2: float = 0.0
        d_sumwx: float = 0.0
        d_sumwx2: float = 0.0
        d_sumwy: float = 0.0
        d_sumwy2: float = 0.0
        d_sumwxy: float = 0.0
        d_numentries: float = 0.0

        ########################################################
        # YODA compatibilty code
        ########################################################

        def fill(self, x: float, y: float, weight: float = 1.0, fraction=1.0):
            sf = fraction * weight
            self.d_sumw += sf
            self.d_sumw2 += sf * weight
            self.d_sumwx += sf * x
            self.d_sumwx2 += sf * x**2
            self.d_sumwy += sf * y
            self.d_sumwy2 += sf * y**2
            self.d_sumwxy += sf * x * y
            self.d_numentries += fraction

        def xMin(self):
            return self.d_xmin

        def xMax(self):
            return self.d_xmax

        def yMin(self):
            return self.d_ymin

        def yMax(self):
            return self.d_ymax

        def sumW(self):
            return self.d_sumw

        def sumW2(self):
            return self.d_sumw2

        def sumWX(self):
            return self.d_sumwx

        def sumWX2(self):
            return self.d_sumwx2

        def sumWY(self):
            return self.d_sumwy

        def sumWY2(self):
            return self.d_sumwy2

        def sumWXY(self):
            return self.d_sumwxy

        def numEntries(self):
            return self.d_numentries

    d_bins: list[Bin] = field(default_factory=list)
    d_overflow: Optional[Bin] = None
    d_underflow: Optional[Bin] = None

    def __post_init__(self):
        self.d_type = "Histo2D"

    #
    # YODA compatibilty code
    #

    def fill(self, x, y, weight=1.0, fraction=1.0):
        for b in self.d_bins:
            if b.d_xmin <= x < b.d_xmax and b.d_ymin <= y < b.d_ymax:
                b.fill(x, y, weight, fraction)
        if x >= self.xMax() and self.d_overflow is not None:
            self.d_overflow.fill(x, y, weight, fraction)
        if x < self.xMin() and self.d_underflow is not None:
            self.d_underflow.fill(x, y, weight, fraction)

    def xMin(self):
        return min(b.d_xmin for b in self.d_bins)

    def xMax(self):
        return max(b.d_xmax for b in self.d_bins)

    def bins(self):
        # sort the bins by xlow, then ylow
        return sorted(self.d_bins, key=lambda b: (b.d_xmin, b.d_ymin))

    def bin(self, index):
        return self.bins()[index]

    def binAt(self, x, y):
        for b in self.bins():
            if b.d_xmin <= x < b.d_xmax and b.d_ymin <= y < b.d_ymax:
                return b
        return None


def parse_histo2d_v2(file_content: str, name: str = "") -> GROGU_HISTO2D_V2:
    lines = file_content.strip().splitlines()

    # Extract metadata (path, title)
    path = ""
    title = ""
    for line in lines:
        if line.startswith("Path:"):
            path = line.split(":")[1].strip()
        elif line.startswith("Title:"):
            title = line.split(":")[1].strip()
        elif line.startswith("---"):
            break

    bins = []
    underflow = overflow = None
    data_section_started = False

    for line in lines:
        if line.startswith("#"):
            continue
        if line.startswith("---"):
            data_section_started = True
            continue
        if not data_section_started:
            continue

        values = re.split(r"\s+", line.strip())
        if values[0] == "Underflow":
            underflow = GROGU_HISTO2D_V2.Bin(
                None,
                None,
                None,
                None,
                float(values[2]),
                float(values[3]),
                float(values[4]),
                float(values[5]),
                float(values[6]),
                float(values[7]),
                float(values[8]),
                float(values[9]),
            )
        elif values[0] == "Overflow":
            overflow = GROGU_HISTO2D_V2.Bin(
                None,
                None,
                None,
                None,
                float(values[2]),
                float(values[3]),
                float(values[4]),
                float(values[5]),
                float(values[6]),
                float(values[7]),
                float(values[8]),
                float(values[9]),
            )
        elif values[0] == "Total":
            pass
        else:
            (
                xlow,
                xhigh,
                ylow,
                yhigh,
                sumw,
                sumw2,
                sumwx,
                sumwx2,
                sumwy,
                sumwy2,
                sumwxy,
                numEntries,
            ) = map(float, values)
            bins.append(
                GROGU_HISTO2D_V2.Bin(
                    xlow,
                    xhigh,
                    ylow,
                    yhigh,
                    sumw,
                    sumw2,
                    sumwx,
                    sumwx2,
                    sumwy,
                    sumwy2,
                    sumwxy,
                    numEntries,
                )
            )

    return GROGU_HISTO2D_V2(
        d_key=name,
        d_path=path,
        d_title=title,
        d_bins=bins,
        d_underflow=underflow,
        d_overflow=overflow,
    )
