import copy
import re
import sys
from dataclasses import dataclass, field

import numpy as np

from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT
from babyyoda.grogu.histo1d_v3 import Histo1D_v3
from babyyoda.histo2d import UHIHisto2D


def to_index(x, y, xedges, yedges):
    # get ix and iy to map to correct bin
    fix = None
    for ix, xEdge in enumerate([*xedges, sys.float_info.max]):
        fix = ix
        if x < xEdge:
            break
    fiy = None
    for iy, yEdge in enumerate([*yedges, sys.float_info.max]):
        fiy = iy
        if y < yEdge:
            break
    # Also fill overflow bins
    return fiy * (len(xedges) + 1) + fix


def Histo2D_v3(
    *args,
    title=None,
    **kwargs,
):
    xedges = []
    yedges = []
    if isinstance(args[0], list) and isinstance(args[1], list):
        xedges = args[0]
        yedges = args[1]
    elif (
        isinstance(args[0], int)
        and isinstance(args[1], (int, float))
        and isinstance(args[2], (int, float))
        and isinstance(args[3], int)
        and isinstance(args[4], (int, float))
        and isinstance(args[5], (int, float))
    ):
        nxbins = args[0]
        xstart = float(args[1])
        xend = float(args[2])
        nybins = args[3]
        ystart = float(args[4])
        yend = float(args[5])
        xedges = [xstart + i * (xend - xstart) / nxbins for i in range(nxbins + 1)]
        yedges = [ystart + i * (yend - ystart) / nybins for i in range(nybins + 1)]
    return GROGU_HISTO2D_V3(
        d_edges=[
            xedges,
            yedges,
        ],
        d_bins=[
            GROGU_HISTO2D_V3.Bin()
            for _ in range(
                (len(xedges) + 1) * (len(yedges) + 1)
            )  # add overflow and underflow
        ],
        d_annotations={"Title": title} if title else {},
        **kwargs,
    )


@dataclass
class GROGU_HISTO2D_V3(GROGU_ANALYSIS_OBJECT, UHIHisto2D):
    @dataclass
    class Bin:
        d_sumw: float = 0.0
        d_sumw2: float = 0.0
        d_sumwx: float = 0.0
        d_sumwx2: float = 0.0
        d_sumwy: float = 0.0
        d_sumwy2: float = 0.0
        d_sumwxy: float = 0.0
        d_numentries: float = 0.0

        def clone(self):
            return GROGU_HISTO2D_V3.Bin(
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

        def crossTerm(self, x, y):
            assert (x == 0 and y == 1) or (x == 1 and y == 0)
            return self.sumWXY()

        def numEntries(self):
            return self.d_numentries

        def __add__(self, other: "GROGU_HISTO2D_V3.Bin") -> "GROGU_HISTO2D_V3.Bin":
            assert isinstance(other, GROGU_HISTO2D_V3.Bin)
            return GROGU_HISTO2D_V3.Bin(
                d_sumw=self.d_sumw + other.d_sumw,
                d_sumw2=self.d_sumw2 + other.d_sumw2,
                d_sumwx=self.d_sumwx + other.d_sumwx,
                d_sumwx2=self.d_sumwx2 + other.d_sumwx2,
                d_sumwy=self.d_sumwy + other.d_sumwy,
                d_sumwy2=self.d_sumwy2 + other.d_sumwy2,
                d_sumwxy=self.d_sumwxy + other.d_sumwxy,
                d_numentries=self.d_numentries + other.d_numentries,
            )

        def to_string(self) -> str:
            return (
                f"{self.d_sumw:<13.6e}\t{self.d_sumw2:<13.6e}\t{self.d_sumwx:<13.6e}\t{self.d_sumwx2:<13.6e}\t"
                f"{self.d_sumwy:<13.6e}\t{self.d_sumwy2:<13.6e}\t{self.d_sumwxy:<13.6e}\t{self.d_numentries:<13.6e}"
            ).strip()

        @classmethod
        def from_string(cls, line: str) -> "GROGU_HISTO2D_V3.Bin":
            values = re.split(r"\s+", line.strip())
            sumw, sumw2, sumwx, sumwx2, sumwy, sumwy2, sumwxy, numEntries = map(
                float, values
            )
            return cls(sumw, sumw2, sumwx, sumwx2, sumwy, sumwy2, sumwxy, numEntries)

    d_bins: list[Bin] = field(default_factory=list)
    d_edges: list[list[float]] = field(default_factory=list)

    def __post_init__(self):
        GROGU_ANALYSIS_OBJECT.__post_init__(self)
        self.setAnnotation("Type", "Histo2D")

        # plus 1 for underflow and overflow
        assert len(self.d_bins) == (len(self.d_edges[0]) + 1) * (
            len(self.d_edges[1]) + 1
        )

    #
    # YODA compatibilty code
    #

    def clone(self):
        return GROGU_HISTO2D_V3(
            d_key=self.d_key,
            d_annotations=self.annotationsDict(),
            d_bins=[b.clone() for b in self.d_bins],
            d_edges=copy.deepcopy(self.d_edges),
        )

    def xEdges(self):
        return self.d_edges[0]

    def yEdges(self):
        return self.d_edges[1]

    def fill(self, x, y, weight=1.0, fraction=1.0):
        # Also fill overflow bins
        self.bins(True)[to_index(x, y, self.xEdges(), self.yEdges())].fill(
            x, y, weight, fraction
        )

    def xMax(self):
        assert max(self.xEdges()) == self.xEdges()[-1], "xMax is not the last edge"
        return self.xEdges()[-1]

    def xMin(self):
        assert min(self.xEdges()) == self.xEdges()[0], "xMin is not the first edge"
        return self.xEdges()[0]

    def yMax(self):
        assert max(self.yEdges()) == self.yEdges()[-1], "yMax is not the last edge"
        return self.yEdges()[-1]

    def yMin(self):
        assert min(self.yEdges()) == self.yEdges()[0], "yMin is not the first edge"
        return self.yEdges()[0]

    def bins(self, includeOverflows=False):
        if includeOverflows:
            return self.d_bins
        # TODO consider represent data always as numpy
        return (
            np.array(self.d_bins)
            .reshape((len(self.yEdges()) + 1, len(self.xEdges()) + 1))[1:-1, 1:-1]
            .flatten()
        )

    def rebinXYTo(self, xedges: list[float], yedges: list[float]):
        # print(f"rebinXYTo : {self.xEdges()} -> {xedges}, {self.yEdges()} -> {yedges}")
        own_xedges = self.xEdges()
        for e in xedges:
            assert e in own_xedges, f"Edge {e} not found in own edges {own_xedges}"
        own_yedges = self.yEdges()
        for e in yedges:
            assert e in own_yedges, f"Edge {e} not found in own edges {own_yedges}"

        # new bins inclusive of overflow and underflow
        new_bins = []
        for _ in range((len(xedges) + 1) * (len(yedges) + 1)):
            new_bins.append(GROGU_HISTO2D_V3.Bin())
        new_hist = np.array(new_bins).reshape((len(yedges) + 1, len(xedges) + 1))
        old_hist = np.array(self.d_bins).reshape(
            (len(self.yEdges()) + 1, len(self.xEdges()) + 1)
        )
        old_xedges = np.array(self.xEdges())
        old_yedges = np.array(self.yEdges())
        new_xedges = np.array(xedges)
        new_yedges = np.array(yedges)

        for i in range(len(xedges) + 1):
            for j in range(len(yedges) + 1):
                if i == 0:
                    x_mask = old_xedges <= new_xedges[0]
                    x_mask = np.concatenate((x_mask, [False]))  # skip overflow
                elif i == len(xedges):
                    x_mask = old_xedges > new_xedges[-1]
                    x_mask = np.concatenate((x_mask, [True]))  # keep underflow
                    # x_mask = x_mask + [True] # keep overflow
                else:
                    x_mask = (old_xedges > new_xedges[i - 1]) & (
                        old_xedges <= new_xedges[i]
                    )
                    x_mask = np.concatenate((x_mask, [False]))  # skip overflow
                    # x_mask = x_mask + [False] # skip overflow
                if j == 0:
                    y_mask = old_yedges <= new_yedges[0]
                    y_mask = np.concatenate((y_mask, [False]))  # skip overflow
                    # y_mask = y_mask + [False] # skip overflow
                elif j == len(yedges):
                    y_mask = old_yedges > new_yedges[-1]
                    y_mask = np.concatenate((y_mask, [True]))  # keep underflow
                    # y_mask = y_mask + [True] # keep overflow
                else:
                    y_mask = (old_yedges > new_yedges[j - 1]) & (
                        old_yedges <= new_yedges[j]
                    )
                    y_mask = np.concatenate((y_mask, [False]))  # skip overflow
                    # y_mask = y_mask + [False] # skip overflow
                new_hist[j, i] = old_hist[y_mask, :][:, x_mask].sum()

        self.d_bins = new_hist.flatten()
        self.d_edges = [xedges, yedges]

        assert len(self.d_bins) == (len(xedges) + 1) * (len(yedges) + 1)

    def rebinXTo(self, xedges: list[float]):
        self.rebinXYTo(xedges, self.yEdges())

    def rebinYTo(self, yedges: list[float]):
        self.rebinXYTo(self.xEdges(), yedges)

    def get_projector(self):
        return Histo1D_v3

    def to_string(self) -> str:
        """Convert a YODA_HISTO2D_V3 object to a formatted string."""
        header = (
            f"BEGIN YODA_HISTO2D_V3 {self.d_key}\n"
            f"{GROGU_ANALYSIS_OBJECT.to_string(self)}"
            f"---\n"
        )

        # TODO stats
        stats = ""
        stats = (
            f"# Mean: ({self.xMean():.6e}, {self.yMean():.6e})\n"
            f"# Integral: {self.integral():.6e}\n"
        )
        edges = ""
        for i, edg in enumerate(self.d_edges):
            listed = ", ".join(f"{float(val):.6e}" for val in edg)
            edges += f"Edges(A{i+1}): [{listed}]\n"

        legend = "# sumW       \tsumW2        \tsumW(A1)     \tsumW2(A1)    \tsumW(A2)     \tsumW2(A2)    \tsumW(A1,A2)  \tnumEntries\n"
        bin_data = "\n".join(b.to_string() for b in self.d_bins)
        footer = "\nEND YODA_HISTO2D_V3"

        return f"{header}{stats}{edges}{legend}{bin_data}{footer}"

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_HISTO2D_V3":
        lines = file_content.strip().splitlines()
        key = ""
        if find := re.search(r"BEGIN YODA_HISTO2D_V3 (\S+)", lines[0]):
            key = find.group(1)

        annotations = GROGU_ANALYSIS_OBJECT.from_string(
            file_content=file_content
        ).d_annotations

        # Extract bins and overflow/underflow
        bins = []
        edges = []
        data_section_started = False

        for line in lines:
            if line.startswith("BEGIN YODA_HISTO2D_V3"):
                continue
            if line.startswith("END YODA_HISTO2D_V3"):
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
                edges += [[float(i) for i in values]]
                continue

            bins.append(cls.Bin.from_string(line))

        # Create and return the YODA_HISTO1D_V2 object
        return cls(
            d_key=key,
            d_annotations=annotations,
            d_bins=bins,
            d_edges=edges,
        )
