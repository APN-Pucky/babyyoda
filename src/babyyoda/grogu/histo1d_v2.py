import re
from dataclasses import dataclass, field
from typing import Optional

from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT
from babyyoda.histo1d import UHIHisto1D


@dataclass
class GROGU_HISTO1D_V2(GROGU_ANALYSIS_OBJECT, UHIHisto1D):
    @dataclass
    class Bin:
        d_xmin: Optional[float] = None
        d_xmax: Optional[float] = None
        d_sumw: float = 0.0
        d_sumw2: float = 0.0
        d_sumwx: float = 0.0
        d_sumwx2: float = 0.0
        d_numentries: float = 0.0

        def __post_init__(self):
            assert (
                self.d_xmin is None or self.d_xmax is None or self.d_xmin < self.d_xmax
            )

        ########################################################
        # YODA compatibilty code
        ########################################################

        def clone(self):
            return GROGU_HISTO1D_V2.Bin(
                d_xmin=self.d_xmin,
                d_xmax=self.d_xmax,
                d_sumw=self.d_sumw,
                d_sumw2=self.d_sumw2,
                d_sumwx=self.d_sumwx,
                d_sumwx2=self.d_sumwx2,
                d_numentries=self.d_numentries,
            )

        def fill(self, x: float, weight: float = 1.0, fraction: float = 1.0) -> bool:
            # if (self.d_xmin is None or x > self.d_xmin) and (self.d_xmax is None or x < self.d_xmax):
            sf = fraction * weight
            self.d_sumw += sf
            self.d_sumw2 += sf * weight
            self.d_sumwx += sf * x
            self.d_sumwx2 += sf * x**2
            self.d_numentries += fraction

        def set_bin(self, bin):
            # TODO allow modify those?
            # self.d_xmin = bin.xMin()
            # self.d_xmax = bin.xMax()
            self.d_sumw = bin.sumW()
            self.d_sumw2 = bin.sumW2()
            self.d_sumwx = bin.sumWX()
            self.d_sumwx2 = bin.sumWX2()
            self.d_numentries = bin.numEntries()

        def set(self, numEntries: float, sumW: list[float], sumW2: list[float]):
            assert len(sumW) == 2
            assert len(sumW2) == 2
            self.d_sumw = sumW[0]
            self.d_sumw2 = sumW2[0]
            self.d_sumwx = sumW[1]
            self.d_sumwx2 = sumW2[1]
            self.d_numentries = numEntries

        def xMin(self):
            return self.d_xmin

        def xMax(self):
            return self.d_xmax

        def xMid(self):
            return (self.d_xmin + self.d_xmax) / 2

        def sumW(self):
            return self.d_sumw

        def sumW2(self):
            return self.d_sumw2

        def sumWX(self):
            return self.d_sumwx

        def sumWX2(self):
            return self.d_sumwx2

        def variance(self):
            if self.d_sumw**2 - self.d_sumw2 == 0:
                return 0
            return abs(
                (self.d_sumw2 * self.d_sumw - self.d_sumw**2)
                / (self.d_sumw**2 - self.d_sumw2)
            )
            # return self.d_sumw2/self.d_numentries - (self.d_sumw/self.d_numentries)**2

        def errW(self):
            return self.d_sumw2**0.5

        def stdDev(self):
            return self.variance() ** 0.5

        def effNumEntries(self):
            return self.sumW() ** 2 / self.sumW2()

        def stdErr(self):
            return self.stdDev() / self.effNumEntries() ** 0.5

        def dVol(self):
            return self.d_xmax - self.d_xmin

        def xVariance(self):
            # return self.d_sumwx2/self.d_sumw - (self.d_sumwx/self.d_sumw)**2
            if self.d_sumw**2 - self.d_sumw2 == 0:
                return 0
            return abs(
                (self.d_sumwx2 * self.d_sumw - self.d_sumwx**2)
                / (self.d_sumw**2 - self.d_sumw2)
            )

        def numEntries(self):
            return self.d_numentries

        # def __eq__(self, other):
        #    return (
        #        isinstance(other, GROGU_HISTO1D_V2.Bin)
        #        and self.d_xmin == other.d_xmin
        #        and self.d_xmax == other.d_xmax
        #        and self.d_sumw == other.d_sumw
        #        and self.d_sumw2 == other.d_sumw2
        #        and self.d_sumwx == other.d_sumwx
        #        and self.d_sumwx2 == other.d_sumwx2
        #        and self.d_numentries == other.d_numentries
        #    )

        def __add__(self, other):
            assert isinstance(other, GROGU_HISTO1D_V2.Bin)
            return GROGU_HISTO1D_V2.Bin(
                self.d_xmin,
                self.d_xmax,
                self.d_sumw + other.d_sumw,
                self.d_sumw2 + other.d_sumw2,
                self.d_sumwx + other.d_sumwx,
                self.d_sumwx2 + other.d_sumwx2,
                self.d_numentries + other.d_numentries,
            )

        @classmethod
        def from_string(cls, line: str) -> "GROGU_HISTO1D_V2.Bin":
            values = re.split(r"\s+", line.strip())
            assert len(values) == 7
            if (
                values[0] == "Underflow"
                or values[0] == "Overflow"
                or values[0] == "Total"
            ):
                return cls(
                    None,
                    None,
                    float(values[2]),
                    float(values[3]),
                    float(values[4]),
                    float(values[5]),
                    float(values[6]),
                )
            return cls(
                float(values[0]),
                float(values[1]),
                float(values[2]),
                float(values[3]),
                float(values[4]),
                float(values[5]),
                float(values[6]),
            )

        def to_string(bin, label=None) -> str:
            """Convert a Histo1DBin object to a formatted string."""
            if label is None:
                return f"{bin.d_xmin:<12.6e}\t{bin.d_xmax:<12.6e}\t{bin.d_sumw:<12.6e}\t{bin.d_sumw2:<12.6e}\t{bin.d_sumwx:<12.6e}\t{bin.d_sumwx2:<12.6e}\t{bin.d_numentries:<12.6e}"
            return f"{label:8}\t{label:8}\t{bin.d_sumw:<12.6e}\t{bin.d_sumw2:<12.6e}\t{bin.d_sumwx:<12.6e}\t{bin.d_sumwx2:<12.6e}\t{bin.d_numentries:<12.6e}"

    d_bins: list[Bin] = field(default_factory=list)
    d_overflow: Optional[Bin] = None
    d_underflow: Optional[Bin] = None
    d_total: Optional[Bin] = None

    def __post_init__(self):
        self.d_type = "Histo1D"

    ############################################
    # YODA compatibilty code
    ############################################

    def clone(self):
        return GROGU_HISTO1D_V2(
            d_key=self.d_key,
            d_path=self.d_path,
            d_scaled_by=self.d_scaled_by,
            d_title=self.d_title,
            d_bins=[b.clone() for b in self.d_bins],
            d_underflow=self.d_underflow,
            d_overflow=self.d_overflow,
            d_total=self.d_total,
        )

    def underflow(self):
        return self.d_underflow

    def overflow(self):
        return self.d_overflow

    def fill(self, x, weight=1.0, fraction=1.0):
        self.d_total.fill(x, weight, fraction)
        for b in self.d_bins:
            if b.xMin() <= x < b.xMax():
                b.fill(x, weight, fraction)
        if x >= self.xMax() and self.d_overflow is not None:
            self.d_overflow.fill(x, weight, fraction)
        if x < self.xMin() and self.d_underflow is not None:
            self.d_underflow.fill(x, weight, fraction)

    def xMax(self):
        return max([b.xMax() for b in self.d_bins])

    def xMin(self):
        return min([b.xMin() for b in self.d_bins])

    def bins(self, includeOverflows=False):
        if includeOverflows:
            return [self.d_underflow, *self.d_bins, self.d_overflow]
        # TODO sorted needed here?
        return sorted(self.d_bins, key=lambda b: b.d_xmin)

    def bin(self, *indices):
        return [self.bins()[i] for i in indices]

    def binAt(self, x):
        for b in self.bins():
            if b.d_xmin <= x < b.d_xmax:
                return b
        return None

    def binDim(self):
        return 1

    def xEdges(self):
        return [b.xMin() for b in self.d_bins] + [self.xMax()]

    def rebinXTo(self, edges: list[float]):
        own_edges = self.xEdges()
        for e in edges:
            assert e in own_edges, f"Edge {e} not found in own edges {own_edges}"

        new_bins = []
        for i in range(len(edges) - 1):
            new_bins.append(GROGU_HISTO1D_V2.Bin(d_xmin=edges[i], d_xmax=edges[i + 1]))
        for b in self.bins():
            if b.xMid() < min(edges):
                self.d_underflow += b
            elif b.xMid() > max(edges):
                self.d_overflow += b
            else:
                for i in range(len(edges) - 1):
                    if edges[i] <= b.xMid() and b.xMid() <= edges[i + 1]:
                        new_bins[i] += b
        self.d_bins = new_bins

        assert len(self.d_bins) == len(self.xEdges()) - 1
        # return self

    def to_string(histo) -> str:
        """Convert a YODA_HISTO1D_V2 object to a formatted string."""
        scale = (
            "" if histo.d_scaled_by == 1.0 else f"ScaledBy: {histo.d_scaled_by:.17e}\n"
        )
        header = (
            f"BEGIN YODA_HISTO1D_V2 {histo.d_key}\n"
            f"Path: {histo.d_path}\n"
            f"{scale}"
            f"Title: {histo.d_title}\n"
            f"Type: Histo1D\n"
            "---\n"
        )

        # Add the sumw and other info (we assume it's present in the metadata but you could also compute)
        stats = f"# Mean: {histo.xMean():.6e}\n" f"# Area: {histo.integral():.6e}\n"

        underflow = histo.d_underflow.to_string("Underflow")
        overflow = histo.d_overflow.to_string("Overflow")
        total = histo.d_total.to_string("Total")

        xlegend = "# ID\t ID\t sumw\t sumw2\t sumwx\t sumwx2\t numEntries\n"
        legend = "# xlow\t xhigh\t sumw\t sumw2\t sumwx\t sumwx2\t numEntries\n"
        # Add the bin data
        bin_data = "\n".join(b.to_string() for b in histo.bins())

        footer = "END YODA_HISTO1D_V2"

        return f"{header}{stats}{xlegend}{total}\n{underflow}\n{overflow}\n{legend}{bin_data}\n{footer}"

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_HISTO1D_V2":
        lines = file_content.strip().splitlines()
        key = ""
        if find := re.search(r"BEGIN YODA_HISTO1D_V2 (\S+)", lines[0]):
            key = find.group(1)

        # Extract metadata (path, title)
        path = ""
        title = ""
        scaled_by = 1.0
        for line in lines:
            if line.startswith("Path:"):
                path = line.split(":")[1].strip()
            elif line.startswith("Title:"):
                title = line.split(":")[1].strip()
            elif line.startswith("ScaledBy:"):
                scaled_by = float(line.split(":")[1].strip())
            elif line.startswith("---"):
                break

        # Extract bins and overflow/underflow
        bins = []
        underflow = overflow = total = None
        data_section_started = False

        for line in lines:
            if line.startswith("BEGIN YODA_HISTO1D_V2"):
                continue
            if line.startswith("END YODA_HISTO1D_V2"):
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
                underflow = cls.Bin.from_string(line)
            elif values[0] == "Overflow":
                overflow = cls.Bin.from_string(line)
            elif values[0] == "Total":
                total = cls.Bin.from_string(line)
            else:
                # Regular bin
                bins.append(cls.Bin.from_string(line))

        # Create and return the YODA_HISTO1D_V2 object
        return cls(
            d_key=key,
            d_path=path,
            d_title=title,
            d_scaled_by=scaled_by,
            d_bins=bins,
            d_underflow=underflow,
            d_total=total,
            d_overflow=overflow,
        )
