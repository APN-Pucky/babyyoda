import re
from dataclasses import dataclass, field
from typing import Optional, Union

from babyyoda.counter import UHICounter
from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT


def Counter_v3(title: Optional[str] = None, **kwargs) -> "GROGU_COUNTER_V3":
    return GROGU_COUNTER_V3(
        d_bins=[GROGU_COUNTER_V3.Bin()],
        d_annotations={"Title": title} if title else {},
        **kwargs,
    )


@dataclass
class GROGU_COUNTER_V3(GROGU_ANALYSIS_OBJECT, UHICounter):
    @dataclass
    class Bin:
        d_sumw: float = 0.0
        d_sumw2: float = 0.0
        d_numentries: float = 0.0

        ########################################################
        # YODA compatibility code
        ########################################################

        def clone(self):
            return GROGU_COUNTER_V3.Bin(
                d_sumw=self.d_sumw,
                d_sumw2=self.d_sumw2,
                d_numentries=self.d_numentries,
            )

        def fill(self, weight: float = 1.0, fraction: float = 1.0) -> bool:
            sf = fraction * weight
            self.d_sumw += sf
            self.d_sumw2 += sf * weight
            self.d_numentries += fraction

        def set_bin(self, bin):
            self.d_sumw = bin.sumW()
            self.d_sumw2 = bin.sumW2()
            self.d_numentries = bin.numEntries()

        def set(
            self,
            numEntries: float,
            sumW: Union[list[float], float],
            sumW2: Union[list[float], float],
        ):
            if isinstance(sumW, float):
                sumW = [sumW]
            if isinstance(sumW2, float):
                sumW2 = [sumW2]
            assert len(sumW) == 1
            assert len(sumW2) == 1
            self.d_sumw = sumW[0]
            self.d_sumw2 = sumW2[0]
            self.d_numentries = numEntries

        def sumW(self) -> float:
            return self.d_sumw

        def sumW2(self) -> float:
            return self.d_sumw2

        def variance(self) -> float:
            if self.d_sumw**2 - self.d_sumw2 == 0:
                return 0
            return abs(
                (self.d_sumw2 * self.d_sumw - self.d_sumw**2)
                / (self.d_sumw**2 - self.d_sumw2)
            )
            # return self.d_sumw2/self.d_numentries - (self.d_sumw/self.d_numentries)**2

        def errW(self) -> float:
            return self.d_sumw2**0.5

        def stdDev(self) -> float:
            return self.variance() ** 0.5

        def effNumEntries(self) -> float:
            return self.sumW() ** 2 / self.sumW2()

        def stdErr(self) -> float:
            return self.stdDev() / self.effNumEntries() ** 0.5

        def numEntries(self) -> float:
            return self.d_numentries

        def __eq__(self, other):
            return (
                isinstance(other, GROGU_COUNTER_V3.Bin)
                and self.d_sumw == other.d_sumw
                and self.d_sumw2 == other.d_sumw2
                and self.d_numentries == other.d_numentries
            )

        def __add__(self, other):
            assert isinstance(other, GROGU_COUNTER_V3.Bin)
            return GROGU_COUNTER_V3.Bin(
                self.d_sumw + other.d_sumw,
                self.d_sumw2 + other.d_sumw2,
                self.d_numentries + other.d_numentries,
            )

        def to_string(self) -> str:
            """Convert a CounterBin object to a formatted string."""
            return f"{self.d_sumw:<13.6e}\t{self.d_sumw2:<13.6e}\t{self.d_numentries:<13.6e}".strip()

        @classmethod
        def from_string(cls, string: str) -> "GROGU_COUNTER_V3.Bin":
            values = re.split(r"\s+", string.strip())
            # Regular bin
            sumw, sumw2, numEntries = map(float, values)
            return cls(sumw, sumw2, numEntries)

    d_bins: list[Bin] = field(default_factory=list)

    def __post_init__(self) -> None:
        GROGU_ANALYSIS_OBJECT.__post_init__(self)
        self.setAnnotation("Type", "Counter")
        assert len(self.d_bins) == 1

    ############################################
    # YODA compatibility code
    ############################################

    def sumW(self) -> float:
        return self.d_bins[0].sumW()

    def sumW2(self) -> float:
        return self.d_bins[0].sumW2()

    def numEntries(self) -> float:
        return self.d_bins[0].numEntries()

    def clone(self):
        return GROGU_COUNTER_V3(
            d_key=self.d_key,
            d_annotations=self.annotationsDict(),
            d_bins=[b.clone() for b in self.d_bins],
        )

    def fill(self, weight=1.0, fraction=1.0):
        for b in self.bins():
            b.fill(weight=weight, fraction=fraction)

    def set(self, *args, **kwargs):
        self.d_bins[0].set(*args, **kwargs)

    def bins(self):
        return self.d_bins

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_COUNTER_V3":
        lines = file_content.strip().splitlines()
        key = ""
        if find := re.search(r"BEGIN YODA_COUNTER_V3 (\S+)", lines[0]):
            key = find.group(1)

        annotations = GROGU_ANALYSIS_OBJECT.from_string(
            file_content=file_content
        ).d_annotations

        # Extract bins and overflow/underflow
        bins = []
        # edges = []
        data_section_started = False

        for line in lines:
            if line.startswith("BEGIN YODA_COUNTER_V3"):
                continue
            if line.startswith("END YODA_COUNTER_V3"):
                break
            if line.startswith("#") or line.isspace():
                continue
            if line.startswith("---"):
                data_section_started = True
                continue
            if not data_section_started:
                continue

            bins.append(cls.Bin.from_string(line))

        return cls(
            d_key=key,
            d_annotations=annotations,
            d_bins=bins,
        )

    def to_string(self):
        """Convert a YODA_COUNTER_V3 object to a formatted string."""
        header = (
            f"BEGIN YODA_COUNTER_V3 {self.d_key}\n"
            f"{GROGU_ANALYSIS_OBJECT.to_string(self)}"
            "---\n"
        )

        # Add the sumw and other info (we assume it's present in the metadata but you could also compute)
        stats = (
            ""  # f"# Mean: {self.xMean():.6e}\n" f"# Integral: {self.integral():.6e}\n"
        )

        # listed = ", ".join(f"{float(val):.6e}" for val in self.d_edges)
        # edges = f"Edges(A1): [{listed}]\n"
        # Add the bin data
        bin_data = "\n".join(GROGU_COUNTER_V3.Bin.to_string(b) for b in self.bins())

        footer = "END YODA_COUNTER_V3"

        return f"{header}{stats}# sumW       \tsumW2        \tnumEntries\n{bin_data}\n{footer}"
