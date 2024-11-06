import re
from dataclasses import dataclass, field
from typing import Any, Optional

from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT
from babyyoda.grogu.histo1d_v2 import Histo1D_v2
from babyyoda.histo2d import UHIHisto2D


def Histo2D_v2(
    *args: Any,
    title: Optional[str] = None,
    **kwargs: Any,
) -> "GROGU_HISTO2D_V2":
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

    return GROGU_HISTO2D_V2(
        d_bins=[
            GROGU_HISTO2D_V2.Bin(
                d_xmin=xedges[i],
                d_xmax=xedges[i + 1],
                d_ymin=yedges[j],
                d_ymax=yedges[j + 1],
            )
            for i in range(len(xedges) - 1)
            for j in range(len(yedges) - 1)
        ],
        d_total=GROGU_HISTO2D_V2.Bin(),
        d_annotations={"Title": title} if title else {},
        **kwargs,
    )


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
        # YODA compatibility code
        ########################################################

        def clone(self) -> "GROGU_HISTO2D_V2.Bin":
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

        def fill(
            self, x: float, y: float, weight: float = 1.0, fraction: float = 1.0
        ) -> None:
            sf = fraction * weight
            self.d_sumw += sf
            self.d_sumw2 += sf * weight
            self.d_sumwx += sf * x
            self.d_sumwx2 += sf * x**2
            self.d_sumwy += sf * y
            self.d_sumwy2 += sf * y**2
            self.d_sumwxy += sf * x * y
            self.d_numentries += fraction

        def set_bin(self, bin: Any) -> None:
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
        ) -> None:
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

        def contains(self, x: float, y: float) -> bool:
            if (
                self.d_xmin is None
                or self.d_xmax is None
                or self.d_ymin is None
                or self.d_ymax is None
            ):
                return False
            return self.d_xmin <= x < self.d_xmax and self.d_ymin <= y < self.d_ymax

        def xMin(self) -> Optional[float]:
            return self.d_xmin

        def xMax(self) -> Optional[float]:
            return self.d_xmax

        def xMid(self) -> Optional[float]:
            if self.d_xmin is None or self.d_xmax is None:
                return None
            return (self.d_xmin + self.d_xmax) / 2

        def yMid(self) -> Optional[float]:
            if self.d_ymin is None or self.d_ymax is None:
                return None
            return (self.d_ymin + self.d_ymax) / 2

        def yMin(self) -> Optional[float]:
            return self.d_ymin

        def yMax(self) -> Optional[float]:
            return self.d_ymax

        def sumW(self) -> float:
            return self.d_sumw

        def sumW2(self) -> float:
            return self.d_sumw2

        def sumWX(self) -> float:
            return self.d_sumwx

        def sumWX2(self) -> float:
            return self.d_sumwx2

        def sumWY(self) -> float:
            return self.d_sumwy

        def sumWY2(self) -> float:
            return self.d_sumwy2

        def sumWXY(self) -> float:
            return self.d_sumwxy

        def dVol(self) -> Optional[float]:
            if (
                self.d_xmin is None
                or self.d_xmax is None
                or self.d_ymin is None
                or self.d_ymax is None
            ):
                return None
            return (self.d_xmax - self.d_xmin) * (self.d_ymax - self.d_ymin)

        def crossTerm(self, x: int, y: int) -> float:
            assert (x == 0 and y == 1) or (x == 1 and y == 0)
            return self.sumWXY()

        def numEntries(self) -> float:
            return self.d_numentries

        def __add__(self, other: "GROGU_HISTO2D_V2.Bin") -> "GROGU_HISTO2D_V2.Bin":
            assert isinstance(other, GROGU_HISTO2D_V2.Bin)
            return GROGU_HISTO2D_V2.Bin(
                d_xmin=self.d_xmin,
                d_xmax=self.d_xmax,
                d_ymin=self.d_ymin,
                d_ymax=self.d_ymax,
                d_sumw=self.d_sumw + other.d_sumw,
                d_sumw2=self.d_sumw2 + other.d_sumw2,
                d_sumwx=self.d_sumwx + other.d_sumwx,
                d_sumwx2=self.d_sumwx2 + other.d_sumwx2,
                d_sumwy=self.d_sumwy + other.d_sumwy,
                d_sumwy2=self.d_sumwy2 + other.d_sumwy2,
                d_sumwxy=self.d_sumwxy + other.d_sumwxy,
                d_numentries=self.d_numentries + other.d_numentries,
            )

        def to_string(self, label: Optional[str] = None) -> str:
            if label is None:
                return (
                    f"{self.d_xmin:<12.6e}\t{self.d_xmax:<12.6e}\t{self.d_ymin:<12.6e}\t{self.d_ymax:<12.6e}\t"
                    f"{self.d_sumw:<12.6e}\t{self.d_sumw2:<12.6e}\t{self.d_sumwx:<12.6e}\t{self.d_sumwx2:<12.6e}\t"
                    f"{self.d_sumwy:<12.6e}\t{self.d_sumwy2:<12.6e}\t{self.d_sumwxy:<12.6e}\t{self.d_numentries:<12.6e}"
                )
            return f"{label:8}\t{label:8}\t{self.d_sumw:<12.6e}\t{self.d_sumw2:<12.6e}\t{self.d_sumwx:<12.6e}\t{self.d_sumwx2:<12.6e}\t{self.d_sumwy:<12.6e}\t{self.d_sumwy2:<12.6e}\t{self.d_sumwxy:<12.6e}\t{self.d_numentries:<12.6e}"

    d_bins: list[Bin] = field(default_factory=list)
    d_total: Bin = field(default_factory=Bin)

    def __post_init__(self) -> None:
        GROGU_ANALYSIS_OBJECT.__post_init__(self)
        self.setAnnotation("Type", "Histo2D")

    #
    # YODA compatibility code
    #

    def clone(self) -> "GROGU_HISTO2D_V2":
        return GROGU_HISTO2D_V2(
            d_key=self.d_key,
            d_annotations=self.annotationsDict(),
            d_bins=[b.clone() for b in self.d_bins],
            d_total=self.d_total.clone(),
        )

    def fill(
        self, x: float, y: float, weight: float = 1.0, fraction: float = 1.0
    ) -> None:
        self.d_total.fill(x, y, weight, fraction)
        for b in self.d_bins:
            if b.contains(x, y):
                b.fill(x, y, weight, fraction)

    def xEdges(self) -> list[float]:
        assert all(
            x == y
            for x, y in zip(
                sorted({b.d_xmin for b in self.d_bins if b.d_xmin is not None})[1:],
                sorted({b.d_xmax for b in self.d_bins if b.d_xmax is not None})[:-1],
            )
        )
        return sorted(
            {b.d_xmin for b in self.d_bins if b.d_xmin is not None} | {self.xMax()}
        )

    def yEdges(self) -> list[float]:
        assert all(
            x == y
            for x, y in zip(
                sorted({b.d_ymin for b in self.d_bins if b.d_ymin is not None})[1:],
                sorted({b.d_ymax for b in self.d_bins if b.d_ymax is not None})[:-1],
            )
        )
        return sorted(
            {b.d_ymin for b in self.d_bins if b.d_ymin is not None} | {self.yMax()}
        )

    def xMin(self) -> float:
        return min(b.d_xmin for b in self.d_bins if b.d_xmin is not None)

    def yMin(self) -> float:
        return min(b.d_ymin for b in self.d_bins if b.d_ymin is not None)

    def xMax(self) -> float:
        return max(b.d_xmax for b in self.d_bins if b.d_xmax is not None)

    def yMax(self) -> float:
        return max(b.d_ymax for b in self.d_bins if b.d_ymax is not None)

    def bins(self, includeOverflows: bool = False) -> list[Bin]:
        if includeOverflows:
            err = "includeFlow=True not supported"
            raise NotImplementedError(err)
        # sort the bins by xlow, then ylow
        # YODA-1
        # return sorted(self.d_bins, key=lambda b: (b.d_xmin, b.d_ymin))
        # YODA-2
        return sorted(self.d_bins, key=lambda b: (b.d_ymin, b.d_xmin))

    def bin(self, index: int) -> Bin:
        return self.bins()[index]

    def binAt(self, x: float, y: float) -> Optional[Bin]:
        for b in self.bins():
            if (
                b.d_xmin is not None
                and b.d_xmax is not None
                and b.d_ymin is not None
                and b.d_ymax is not None
                and b.d_xmin <= x < b.d_xmax
                and b.d_ymin <= y < b.d_ymax
            ):
                return b
        return None

    def rebinXYTo(self, xedges: list[float], yedges: list[float]) -> None:
        own_xedges = self.xEdges()
        for e in xedges:
            assert e in own_xedges, f"Edge {e} not found in own edges {own_xedges}"
        own_yedges = self.yEdges()
        for e in yedges:
            assert e in own_yedges, f"Edge {e} not found in own edges {own_yedges}"

        new_bins = []
        for j in range(len(yedges) - 1):
            for i in range(len(xedges) - 1):
                new_bins.append(
                    GROGU_HISTO2D_V2.Bin(
                        d_xmin=xedges[i],
                        d_xmax=xedges[i + 1],
                        d_ymin=yedges[j],
                        d_ymax=yedges[j + 1],
                    )
                )
        for b in self.bins():
            for j in range(len(yedges) - 1):
                for i in range(len(xedges) - 1):
                    xm = b.xMid()
                    ym = b.yMid()
                    if (
                        xm
                        and ym
                        and xedges[i] <= xm < xedges[i + 1]
                        and yedges[j] <= ym < yedges[j + 1]
                    ):
                        assert new_bins[i + j * (len(xedges) - 1)].d_xmin == xedges[i]
                        assert (
                            new_bins[i + j * (len(xedges) - 1)].d_xmax == xedges[i + 1]
                        )
                        assert new_bins[i + j * (len(xedges) - 1)].d_ymin == yedges[j]
                        assert (
                            new_bins[i + j * (len(xedges) - 1)].d_ymax == yedges[j + 1]
                        )
                        assert new_bins[i + j * (len(xedges) - 1)].d_xmin is not None
                        assert new_bins[i + j * (len(xedges) - 1)].d_xmax is not None
                        assert new_bins[i + j * (len(xedges) - 1)].contains(xm, ym)
                        new_bins[i + j * (len(xedges) - 1)] += b
        self.d_bins = new_bins

        assert len(self.d_bins) == (len(self.xEdges()) - 1) * (len(self.yEdges()) - 1)

    def rebinXTo(self, xedges: list[float]) -> None:
        self.rebinXYTo(xedges, self.yEdges())

    def rebinYTo(self, yedges: list[float]) -> None:
        self.rebinXYTo(self.xEdges(), yedges)

    def get_projector(self) -> Any:
        return Histo1D_v2

    def to_string(self) -> str:
        """Convert a YODA_HISTO2D_V2 object to a formatted string."""
        header = (
            f"BEGIN YODA_HISTO2D_V2 {self.d_key}\n"
            f"{GROGU_ANALYSIS_OBJECT.to_string(self)}"
            f"---\n"
        )

        # TODO stats
        stats = ""
        stats = (
            f"# Mean: ({self.xMean(includeOverflows=False):.6e}, {self.yMean(includeOverflows=False):.6e})\n"
            f"# Volume: {self.integral(includeOverflows=False):.6e}\n"
        )

        xlegend = "# ID\t ID\t sumw\t sumw2\t sumwx\t sumwx2\t sumwy\t sumwy2\t sumwxy\t numEntries\n"
        total = self.d_total.to_string("Total")

        legend = "# 2D outflow persistency not currently supported until API is stable\n# xlow\t xhigh\t ylow\t yhigh\t sumw\t sumw2\t sumwx\t sumwx2\t sumwy\t sumwy2\t sumwxy\t numEntries\n"
        bin_data = "\n".join(b.to_string() for b in self.d_bins)
        footer = "\nEND YODA_HISTO2D_V2"

        return f"{header}{stats}{xlegend}{total}\n{legend}{bin_data}{footer}"

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_HISTO2D_V2":
        lines = file_content.strip().splitlines()

        key = ""
        if find := re.search(r"BEGIN YODA_HISTO2D_V2 (\S+)", lines[0]):
            key = find.group(1)

        annotations = GROGU_ANALYSIS_OBJECT.from_string(
            file_content=file_content
        ).d_annotations

        bins = []
        total = None
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
            if values[0] == "Underflow" or values[0] == "Overflow":
                pass
            elif values[0] == "Total":
                total = cls.Bin(
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
        if total is not None:
            return cls(
                d_key=key,
                d_annotations=annotations,
                d_bins=bins,
                d_total=total,
            )
        err = "Total bin not found in the histogram"
        raise ValueError(err)
