import copy
import re
from dataclasses import dataclass, field

from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT
from babyyoda.histo1d import UHIHisto1D


@dataclass
class GROGU_HISTO1D_V3(GROGU_ANALYSIS_OBJECT, UHIHisto1D):
    @dataclass
    class Bin:
        d_sumw: float = 0.0
        d_sumw2: float = 0.0
        d_sumwx: float = 0.0
        d_sumwx2: float = 0.0
        d_numentries: float = 0.0

        ########################################################
        # YODA compatibilty code
        ########################################################

        def clone(self):
            return GROGU_HISTO1D_V3.Bin(
                d_sumw=self.d_sumw,
                d_sumw2=self.d_sumw2,
                d_sumwx=self.d_sumwx,
                d_sumwx2=self.d_sumwx2,
                d_numentries=self.d_numentries,
            )

        def fill(self, x: float, weight: float = 1.0, fraction: float = 1.0) -> bool:
            sf = fraction * weight
            self.d_sumw += sf
            self.d_sumw2 += sf * weight
            self.d_sumwx += sf * x
            self.d_sumwx2 += sf * x**2
            self.d_numentries += fraction

        def set_bin(self, bin):
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

        # def xMin(self):
        #    return self.d_xmin

        # def xMax(self):
        #    return self.d_xmax

        # def xMid(self):
        #    return (self.d_xmin + self.d_xmax) / 2

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
                isinstance(other, GROGU_HISTO1D_V3.Bin)
                and self.d_sumw == other.d_sumw
                and self.d_sumw2 == other.d_sumw2
                and self.d_sumwx == other.d_sumwx
                and self.d_sumwx2 == other.d_sumwx2
                and self.d_numentries == other.d_numentries
            )

        def __add__(self, other):
            assert isinstance(other, GROGU_HISTO1D_V3.Bin)
            return GROGU_HISTO1D_V3.Bin(
                self.d_sumw + other.d_sumw,
                self.d_sumw2 + other.d_sumw2,
                self.d_sumwx + other.d_sumwx,
                self.d_sumwx2 + other.d_sumwx2,
                self.d_numentries + other.d_numentries,
            )

        def to_string(self) -> str:
            """Convert a Histo1DBin object to a formatted string."""
            return f"{self.d_sumw:<13.6e}\t{self.d_sumw2:<13.6e}\t{self.d_sumwx:<13.6e}\t{self.d_sumwx2:<13.6e}\t{self.d_numentries:<13.6e}".strip()

        @classmethod
        def from_string(cls, string: str) -> "GROGU_HISTO1D_V3.Bin":
            values = re.split(r"\s+", string.strip())
            # Regular bin
            sumw, sumw2, sumwx, sumwx2, numEntries = map(float, values)
            return cls(sumw, sumw2, sumwx, sumwx2, numEntries)

    d_edges: list[float] = field(default_factory=list)
    d_bins: list[Bin] = field(default_factory=list)

    def __post_init__(self):
        self.d_type = "Histo1D"
        # one more edge than bins, subtract 2 for underflow and overflow
        assert (
            len(self.d_edges) == len(self.d_bins) + 1 - 2
        ), f"{len(self.d_edges)} != {len(self.d_bins)} + 1 - 2"

    ############################################
    # YODA compatibilty code
    ############################################

    def clone(self):
        return GROGU_HISTO1D_V3(
            d_key=self.d_key,
            d_path=self.d_path,
            d_scaled_by=self.d_scaled_by,
            d_title=self.d_title,
            d_edges=copy.deepcopy(self.d_edges),
            d_bins=[b.clone() for b in self.d_bins],
        )

    def underflow(self):
        return self.bins(includeOverflows=True)[0]

    def overflow(self):
        return self.bins(includeOverflows=True)[-1]

    def fill(self, x, weight=1.0, fraction=1.0):
        for i, b in enumerate(self.bins()):
            if self.xEdges()[i] <= x < self.xEdges()[i + 1]:
                b.fill(x, weight, fraction)
        if x >= self.xMax():
            self.overflow().fill(x, weight, fraction)
        if x < self.xMin():
            self.underflow().fill(x, weight, fraction)

    def xMax(self):
        return max(self.xEdges())

    def xMin(self):
        return min(self.xEdges())

    def bins(self, includeOverflows=False):
        return self.d_bins[1:-1] if not includeOverflows else self.d_bins

    def bin(self, *indices):
        return [self.bins()[i] for i in indices]

    def binAt(self, x):
        # TODO add tests for binAt
        for i, b in enumerate(self.bins()):
            if self.xEdges()[i] <= x < self.xEdges()[i + 1]:
                return b
        return None

    def binDim(self):
        return 1

    def xEdges(self):
        return self.d_edges

    def xMid(self, i):
        return (self.xEdges()[i] + self.xEdges()[i + 1]) / 2

    def rebinXTo(self, edges: list[float]):
        own_edges = self.xEdges()
        for e in edges:
            assert e in own_edges, f"Edge {e} not found in own edges {own_edges}"

        new_bins = []
        of = self.overflow()
        uf = self.underflow()
        for _i in range(len(edges) - 1):
            new_bins.append(GROGU_HISTO1D_V3.Bin())
        for i, b in enumerate(self.bins()):
            if self.xMid(i) < min(edges):
                uf += b
            elif self.xMid(i) > max(edges):
                of += b
            else:
                for j in range(len(edges) - 1):
                    if edges[j] <= self.xMid(i) and self.xMid(i) <= edges[j + 1]:
                        new_bins[j] += b
        self.d_bins = [uf, *new_bins, of]
        self.d_edges = edges

        assert len(self.d_bins) == len(self.xEdges()) - 1 + 2

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_HISTO1D_V3":
        lines = file_content.strip().splitlines()
        key = ""
        if find := re.search(r"BEGIN YODA_HISTO1D_V3 (\S+)", lines[0]):
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
        edges = []
        data_section_started = False

        for line in lines:
            if line.startswith("BEGIN YODA_HISTO1D_V3"):
                continue
            if line.startswith("END YODA_HISTO1D_V3"):
                break
            if line.startswith("#") or line.isspace():
                continue
            if line.startswith("---"):
                data_section_started = True
                continue
            if not data_section_started:
                continue

            if line.startswith("Edges"):
                content = re.findall(r"\[(.*?)\]", line)[0]
                values = re.split(r"\s+", content.replace(",", ""))
                edges = [float(i) for i in values]
                continue

            bins.append(cls.Bin.from_string(line))

        # Create and return the YODA_HISTO1D_V2 object
        return cls(
            d_key=key,
            d_path=path,
            d_scaled_by=scaled_by,
            d_title=title,
            d_bins=bins,
            d_edges=edges,
        )

    def to_string(self):
        """Convert a YODA_HISTO1D_V3 object to a formatted string."""
        scale = (
            "" if self.d_scaled_by == 1.0 else f"ScaledBy: {self.d_scaled_by:.17e}\n"
        )
        header = (
            f"BEGIN YODA_HISTO1D_V3 {self.d_key}\n"
            f"Path: {self.d_path}\n"
            f"{scale}"
            f"Title: {self.d_title}\n"
            f"Type: Histo1D\n"
            "---\n"
        )

        # Add the sumw and other info (we assume it's present in the metadata but you could also compute)
        stats = f"# Mean: {self.xMean():.6e}\n" f"# Integral: {self.integral():.6e}\n"

        listed = ", ".join(f"{float(val):.6e}" for val in self.d_edges)
        edges = f"Edges(A1): [{listed}]\n"
        # Add the bin data
        bin_data = "\n".join(GROGU_HISTO1D_V3.Bin.to_string(b) for b in self.bins(True))

        footer = "END YODA_HISTO1D_V3"

        return f"{header}{stats}{edges}# sumW       \tsumW2        \tsumW(A1)     \tsumW2(A1)    \tnumEntries\n{bin_data}\n{footer}"
