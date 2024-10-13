import re
from dataclasses import dataclass, field
from typing import Optional

from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT
from babyyoda.histo2d import UHIHisto2D


@dataclass
class GROGU_HISTO2D_V2(GROGU_ANALYSIS_OBJECT, UHIHisto2D):
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

        def clone(self):
            return GROGU_HISTO2D_V2.Bin(
                d_xmin=self.d_xmin,
                d_xmax=self.d_xmax,
                d_ymin=self.d_ymin,
                d_ymax=self.d_ymax,
                d_sumw=self.d_sumw,
                d_sumw2=self.d_sumw2,
                d_sumwx=self.d_sumwx,
                d_sumwx2=self.d_sumwx2,
                d_sumwy=self.d_sumwy,
                d_sumwy2=self.d_sumwy2,
                d_sumwxy=self.d_sumwxy,
                d_numentries=self.d_numentries,
            )

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

        def set_bin(self, bin):
            self.d_sumw = bin.sumW()
            self.d_sumw2 = bin.sumW2()
            self.d_sumwx = bin.sumWX()
            self.d_sumwx2 = bin.sumWX2()
            self.d_sumwy = bin.sumWY()
            self.d_sumwy2 = bin.sumWY2()
            self.d_sumwxy = bin.sumWXY()
            self.d_numentries = bin.numEntries()

        def set(
            self,
            numEntries: float,
            sumW: list[float],
            sumW2: list[float],
            sumWcross: list[float],
        ):
            assert len(sumW) == 3
            assert len(sumW2) == 3
            assert len(sumWcross) == 1
            self.d_sumw = sumW[0]
            self.d_sumw2 = sumW2[0]
            self.d_sumwx = sumW[1]
            self.d_sumwx2 = sumW2[1]
            self.d_sumwy = sumW[2]
            self.d_sumwy2 = sumW2[2]
            self.d_sumwxy = sumWcross[0]
            self.d_numentries = numEntries

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

        def dVol(self):
            return (self.d_xmax - self.d_xmin) * (self.d_ymax - self.d_ymin)

        def crossTerm(self, x, y):
            assert (x == 0 and y == 1) or (x == 1 and y == 0)
            return self.sumWXY()

        def numEntries(self):
            return self.d_numentries

        def to_string(self) -> str:
            return (
                f"{self.d_xmin:.6e}\t{self.d_xmax:.6e}\t{self.d_ymin:.6e}\t{self.d_ymax:.6e}\t"
                f"{self.d_sumw:.6e}\t{self.d_sumw2:.6e}\t{self.d_sumwx:.6e}\t{self.d_sumwx2:.6e}\t"
                f"{self.d_sumwy:.6e}\t{self.d_sumwy2:.6e}\t{self.d_sumwxy:.6e}\t{self.d_numentries:.6e}"
            )

    d_bins: list[Bin] = field(default_factory=list)
    d_overflow: Optional[Bin] = None
    d_underflow: Optional[Bin] = None

    def __post_init__(self):
        self.d_type = "Histo2D"

    #
    # YODA compatibilty code
    #

    def clone(self):
        return GROGU_HISTO2D_V2(
            d_key=self.d_key,
            d_path=self.d_path,
            d_title=self.d_title,
            d_bins=[b.clone() for b in self.d_bins],
            d_underflow=self.d_underflow,
            d_overflow=self.d_overflow,
        )

    def fill(self, x, y, weight=1.0, fraction=1.0):
        for b in self.d_bins:
            if b.d_xmin <= x < b.d_xmax and b.d_ymin <= y < b.d_ymax:
                b.fill(x, y, weight, fraction)
        if x >= self.xMax() and self.d_overflow is not None:
            self.d_overflow.fill(x, y, weight, fraction)
        if x < self.xMin() and self.d_underflow is not None:
            self.d_underflow.fill(x, y, weight, fraction)

    def xEdges(self):
        assert all(
            x == y
            for x, y in zip(
                sorted({b.d_xmin for b in self.d_bins})[1:],
                sorted({b.d_xmax for b in self.d_bins})[:-1],
            )
        )
        return sorted({b.d_xmin for b in self.d_bins} + {self.xMax()})

    def yEdges(self):
        assert all(
            x == y
            for x, y in zip(
                sorted({b.d_ymin for b in self.d_bins})[1:],
                sorted({b.d_ymax for b in self.d_bins})[:-1],
            )
        )
        return sorted({b.d_ymin for b in self.d_bins} + {self.yMax()})

    def xMin(self):
        return min(b.d_xmin for b in self.d_bins)

    def yMin(self):
        return min(b.d_ymin for b in self.d_bins)

    def xMax(self):
        return max(b.d_xmax for b in self.d_bins)

    def yMax(self):
        return max(b.d_ymax for b in self.d_bins)

    def bins(self, includeFlow=False):
        if includeFlow:
            err = "includeFlow=True not supported"
            raise NotImplementedError(err)
        # sort the bins by xlow, then ylow
        # YODA-1
        # return sorted(self.d_bins, key=lambda b: (b.d_xmin, b.d_ymin))
        # YODA-2
        return sorted(self.d_bins, key=lambda b: (b.d_ymin, b.d_xmin))

    def bin(self, index):
        return self.bins()[index]

    def binAt(self, x, y):
        for b in self.bins():
            if b.d_xmin <= x < b.d_xmax and b.d_ymin <= y < b.d_ymax:
                return b
        return None

    def to_string(self) -> str:
        """Convert a YODA_HISTO2D_V2 object to a formatted string."""
        header = (
            f"BEGIN YODA_HISTO2D_V2 {self.d_key}\n"
            f"Path: {self.d_path}\n"
            f"Title: {self.d_title}\n"
            f"Type: {self.d_type}\n"
            f"---\n"
        )

        # TODO stats
        stats = ""
        # stats= (
        #    f"# Mean: {self.mean()}\n"
        #    f"# Area: {self.area()}\n"
        # )

        legend = "# xlow\t xhigh\t ylow\t yhigh\t sumw\t sumw2\t sumwx\t sumwx2\t sumwy\t sumwy2\t sumwxy\t numEntries\n"
        bin_data = "\n".join(b.to_string() for b in self.d_bins)
        footer = "\nEND YODA_HISTO2D_V2\n"

        return f"{header}{stats}{legend}{bin_data}{footer}"

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_HISTO2D_V2":
        lines = file_content.strip().splitlines()

        key = ""
        if find := re.search(r"BEGIN YODA_HISTO2D_V2 (\S+)", lines[0]):
            key = find.group(1)

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
            if line.startswith("BEGIN YODA_HISTO2D_V2"):
                continue
            if line.startswith("END YODA_HISTO2D_V2"):
                break
            if line.startswith("#") or line.isspace():
                continue
            if line.startswith("---"):
                data_section_started = True
                continue
            if not data_section_started:
                continue

            values = re.split(r"\s+", line.strip())
            if values[0] == "Underflow":
                underflow = cls.Bin(
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
                overflow = cls.Bin(
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
                    cls.Bin(
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

        return cls(
            d_key=key,
            d_path=path,
            d_title=title,
            d_bins=bins,
            d_underflow=underflow,
            d_overflow=overflow,
        )
