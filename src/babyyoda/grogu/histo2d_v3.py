import re
from dataclasses import dataclass, field
import sys
from typing import List

import numpy as np

from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT


@dataclass
class GROGU_HISTO2D_V3(GROGU_ANALYSIS_OBJECT):
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
            sumW: List[float],
            sumW2: List[float],
            sumWcross: List[float],
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

        def to_string(self) -> str:
            return (
                f"{self.d_sumw:.6e}\t{self.d_sumw2:.6e}\t{self.d_sumwx:.6e}\t{self.d_sumwx2:.6e}\t"
                f"{self.d_sumwy:.6e}\t{self.d_sumwy2:.6e}\t{self.d_sumwxy:.6e}\t{self.d_numentries:.6e}"
            )

        @classmethod
        def from_string(cls, line: str) -> "GROGU_HISTO2D_V3.Bin":
            values = re.split(r"\s+", line.strip())
            sumw, sumw2, sumwx, sumwx2, sumwy, sumwy2, sumwxy, numEntries = map(
                float, values
            )
            return cls(sumw, sumw2, sumwx, sumwx2, sumwy, sumwy2, sumwxy, numEntries)

    d_bins: List[Bin] = field(default_factory=list)
    d_edges: List[List[float]] = field(default_factory=list)

    def __post_init__(self):
        self.d_type = "Histo2D"

        # plus 1 for underflow and overflow
        assert len(self.d_bins) == (len(self.d_edges[0]) + 1) * (
            len(self.d_edges[1]) + 1
        )

    #
    # YODA compatibilty code
    #

    def xEdges(self):
        return self.d_edges[0]

    def yEdges(self):
        return self.d_edges[1]

    def fill(self, x, y, weight=1.0, fraction=1.0):
        # get ix and iy to map to correct bin
        for ix, xEdge in enumerate(self.xEdges() + [sys.float_info.max]):
            if x < xEdge:
                break
        for iy, yEdge in enumerate(self.yEdges() + [sys.float_info.max]):
            if y < yEdge:
                break
        # Also fill overflow bins
        self.bins(True)[iy * (len(self.xEdges()) + 1) + ix].fill(x, y, weight, fraction)

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

    def bins(self, includeFlows=False):
        if includeFlows:
            return self.d_bins
        # TODO consider represent data always as numpy
        return (
            np.array(self.d_bins)
            .reshape((len(self.yEdges()) + 1, len(self.xEdges()) + 1))[1:-1, 1:-1]
            .flatten()
        )

    def to_string(self) -> str:
        """Convert a YODA_HISTO2D_V3 object to a formatted string."""
        header = (
            f"BEGIN YODA_HISTO2D_V3 {self.d_key}\n"
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

        legend = (
            "# sumw\t sumw2\t sumwx\t sumwx2\t sumwy\t sumwy2\t sumwxy\t numEntries\n"
        )
        bin_data = "\n".join(b.to_string() for b in self.d_bins)
        footer = "END YODA_HISTO2D_V3\n"

        return f"{header}{stats}{legend}{bin_data}{footer}"

    @classmethod
    def from_string(cls, file_content: str, key: str = "") -> "GROGU_HISTO2D_V3":
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
        edges = []
        data_section_started = False

        for line in lines:
            if line.startswith("#"):
                continue
            if line.startswith("---"):
                data_section_started = True
                continue
            if not data_section_started:
                continue

            if line.startswith("Edges"):
                content = re.findall(r"\[(.*?)\]", line)
                numbers_as_strings = re.findall(
                    r"[-+]?\d*\.\d+e[+-]?\d+|\d+", content[0]
                )
                edges += [[float(i) for i in numbers_as_strings]]
                continue

            bins.append(GROGU_HISTO2D_V3.Bin.from_string(line))

        # Create and return the YODA_HISTO1D_V2 object
        return GROGU_HISTO2D_V3(
            d_key=key,
            d_path=path,
            d_title=title,
            d_bins=bins,
            d_edges=edges,
        )
