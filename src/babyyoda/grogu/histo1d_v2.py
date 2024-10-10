import re
from typing import List, Optional
from dataclasses import dataclass, field

from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT


@dataclass
class GROGU_HISTO1D_V2(GROGU_ANALYSIS_OBJECT):
    @dataclass
    class Bin:
        d_xmin: Optional[float] = None
        d_xmax: Optional[float] = None
        d_sumw: float = 0.0
        d_sumw2: float = 0.0
        d_sumwx: float = 0.0
        d_sumwx2: float = 0.0
        d_numentries: float = 0.0

        ########################################################
        # YODA compatibilty code
        ########################################################

        # TODO drop either clone or copy
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

        def copy(self):
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

        def set(self, numEntries: float, sumW: List[float], sumW2: List[float]):
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

        def __eq__(self, other):
            return (
                isinstance(other, GROGU_HISTO1D_V2.Bin)
                and self.d_xmin == other.d_xmin
                and self.d_xmax == other.d_xmax
                and self.d_sumw == other.d_sumw
                and self.d_sumw2 == other.d_sumw2
                and self.d_sumwx == other.d_sumwx
                and self.d_sumwx2 == other.d_sumwx2
                and self.d_numentries == other.d_numentries
            )

        def __add__(self, other):
            assert isinstance(other, GROGU_HISTO1D_V2.Bin)
            ## combine if the bins are adjacent
            # if self.d_xmax == other.d_xmin:
            #    nxlow = self.d_xmin
            #    nxhigh = other.d_xmax
            # elif self.d_xmin == other.d_xmax:
            #    nxlow = other.d_xmin
            #    nxhigh = self.d_xmax
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
            if values[0] == "Underflow" or values[0] == "Overflow":
                return cls(
                    None,
                    None,
                    float(values[2]),
                    float(values[3]),
                    float(values[4]),
                    float(values[5]),
                    float(values[6]),
                )
            else:
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
                return f"{bin.d_xmin:.6e}\t{bin.d_xmax:.6e}\t{bin.d_sumw:.6e}\t{bin.d_sumw2:.6e}\t{bin.d_sumwx:.6e}\t{bin.d_sumwx2:.6e}\t{bin.d_numentries:.6e}"
            else:
                return f"{label}\t{label}\t{bin.d_sumw:.6e}\t{bin.d_sumw2:.6e}\t{bin.d_sumwx:.6e}\t{bin.d_sumwx2:.6e}\t{bin.d_numentries:.6e}"

    d_bins: List[Bin] = field(default_factory=list)
    d_overflow: Optional[Bin] = None
    d_underflow: Optional[Bin] = None

    def __post_init__(self):
        self.d_type = "Histo1D"

    ############################################
    # YODA compatibilty code
    ############################################

    def clone(self):
        return GROGU_HISTO1D_V2(
            d_key=self.d_key,
            d_path=self.d_path,
            d_title=self.d_title,
            d_bins=[b.copy() for b in self.d_bins],
            d_underflow=self.d_underflow,
            d_overflow=self.d_overflow,
        )

    def underflow(self):
        return self.d_underflow

    def overflow(self):
        return self.d_overflow

    def fill(self, x, weight=1.0, fraction=1.0):
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

    def bins(self):
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

    def rebinXTo(self, edges: List[float]):
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
        header = (
            f"BEGIN YODA_HISTO1D_V2 {histo.d_key}\n"
            f"Path: {histo.d_path}\n"
            f"Title: {histo.d_title}\n"
            f"Type: Histo1D\n"
            "---\n"
        )

        # Add the sumw and other info (we assume it's present in the metadata but you could also compute)
        stats = (
            f"# Mean: {sum(b.d_sumwx for b in histo.d_bins) / sum(b.d_sumw for b in histo.d_bins):.6e}\n"
            f"# Area: {sum(b.d_sumw for b in histo.d_bins):.6e}\n"
        )

        underflow = histo.d_underflow.to_string("Underflow")
        overflow = histo.d_overflow.to_string("Overflow")

        legend = "# xlow\t xhigh\t sumw\t sumw2\t sumwx\t sumwx2\t numEntries\n"
        # Add the bin data
        bin_data = "\n".join(b.to_string() for b in histo.bins())

        footer = "END YODA_HISTO1D_V2\n"

        return f"{header}{stats}{underflow}\n{overflow}\n{legend}{bin_data}\n{footer}"

    @classmethod
    def from_string(cls, file_content: str, key: str = "") -> "GROGU_HISTO1D_V2":
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

        # Extract bins and overflow/underflow
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
                underflow = GROGU_HISTO1D_V2.Bin.from_string(line)
            elif values[0] == "Overflow":
                overflow = GROGU_HISTO1D_V2.Bin.from_string(line)
            elif values[0] == "Total":
                # ignore for now
                pass
            else:
                # Regular bin
                bins.append(GROGU_HISTO1D_V2.Bin.from_string(line))

        # Create and return the YODA_HISTO1D_V2 object
        return GROGU_HISTO1D_V2(
            d_key=key,
            d_path=path,
            d_title=title,
            d_bins=bins,
            d_underflow=underflow,
            d_overflow=overflow,
        )
