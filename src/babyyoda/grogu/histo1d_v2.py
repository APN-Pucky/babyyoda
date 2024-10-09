import re
from typing import Optional
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

        def fill(self, x: float, weight: float = 1.0, fraction: float = 1.0) -> bool:
            # if (self.d_xmin is None or x > self.d_xmin) and (self.d_xmax is None or x < self.d_xmax):
            sf = fraction * weight
            self.d_sumw += sf
            self.d_sumw2 += sf * weight
            self.d_sumwx += sf * x
            self.d_sumwx2 += sf * x**2
            self.d_numentries += fraction

        def xMin(self):
            return self.d_xmin

        def xMax(self):
            return self.d_xmax

        def sumW(self):
            return self.d_sumw

        def sumW2(self):
            return self.d_sumw2

        def sumWX(self):
            return self.d_sumwx

        def sumWX2(self):
            return self.d_sumwx2

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
            nxhigh = None
            nxlow = None
            # combine if the bins are adjacent
            if self.d_xmax == other.d_xmin:
                nxlow = self.d_xmin
                nxhigh = other.d_xmax
            elif self.d_xmin == other.d_xmax:
                nxlow = other.d_xmin
                nxhigh = self.d_xmax
            return GROGU_HISTO1D_V2.Bin(
                nxlow,
                nxhigh,
                self.d_sumw + other.d_sumw,
                self.d_sumw2 + other.d_sumw2,
                self.d_sumwx + other.d_sumwx,
                self.d_sumwx2 + other.d_sumwx2,
                self.d_numentries + other.d_numentries,
            )

    d_bins: list[Bin] = field(default_factory=list)
    d_overflow: Optional[Bin] = None
    d_underflow: Optional[Bin] = None

    def __post_init__(self):
        self.d_type = "Histo1D"

    ############################################
    # YODA compatibilty code
    ############################################

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

    def rebinBy(self, factor: int, start: None, stop: None):
        if start is None:
            start = 0
        if stop is None:
            stop = len(self.bins())
        new_bins = []
        for i in range(start, stop, factor):
            nb = self.bins[i]
            for j in range(1, factor):
                nb += self.bins[i + j]
            new_bins.append(nb)
        return GROGU_HISTO1D_V2(
            d_key=self.d_key,
            d_path=self.d_path,
            d_title=self.d_title,
            d_bins=new_bins,
            d_underflow=self.d_underflow,
            d_overflow=self.d_overflow,
        )

    def rebinTo(bins):
        raise NotImplementedError


def parse_histo1d_v2(file_content: str, key: str = "") -> GROGU_HISTO1D_V2:
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
            underflow = GROGU_HISTO1D_V2.Bin(
                None,
                None,
                float(values[2]),
                float(values[3]),
                float(values[4]),
                float(values[5]),
                float(values[6]),
            )
        elif values[0] == "Overflow":
            overflow = GROGU_HISTO1D_V2.Bin(
                None,
                None,
                float(values[2]),
                float(values[3]),
                float(values[4]),
                float(values[5]),
                float(values[6]),
            )
        elif values[0] == "Total":
            # ignore for now
            pass
        else:
            # Regular bin
            xlow, xhigh, sumw, sumw2, sumwx, sumwx2, numEntries = map(float, values)
            bins.append(
                GROGU_HISTO1D_V2.Bin(
                    xlow, xhigh, sumw, sumw2, sumwx, sumwx2, numEntries
                )
            )

    # Create and return the YODA_HISTO1D_V2 object
    return GROGU_HISTO1D_V2(
        d_key=key,
        d_path=path,
        d_title=title,
        d_bins=bins,
        d_underflow=underflow,
        d_overflow=overflow,
    )


def histo1dbin_to_str(bin: GROGU_HISTO1D_V2.Bin) -> str:
    """Convert a Histo1DBin object to a formatted string."""
    return f"{bin.xlow:.6e}\t{bin.xhigh:.6e}\t{bin.sumw:.6e}\t{bin.sumw2:.6e}\t{bin.sumwx:.6e}\t{bin.sumwx2:.6e}\t{bin.numEntries:.6e}"


def underflow_overflow_to_str(bin: GROGU_HISTO1D_V2.Bin, label: str) -> str:
    """Convert an underflow or overflow bin to a formatted string."""
    return f"{label}\t{label}\t{bin.sumw:.6e}\t{bin.sumw2:.6e}\t{bin.sumwx:.6e}\t{bin.sumwx2:.6e}\t{bin.numEntries:.6e}"


def yoda_histo1d_to_str(histo: GROGU_HISTO1D_V2) -> str:
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
        f"# Mean: {sum(b.d_sumwx for b in histo.d_bins) / sum(b.sumw for b in histo.d_bins):.6e}\n"
        f"# Area: {sum(b.d_sumw for b in histo.d_bins):.6e}\n"
    )

    underflow = underflow_overflow_to_str(histo.underflow_value, "Underflow")
    overflow = underflow_overflow_to_str(histo.overflow_value, "Overflow")

    # Add the bin data
    bin_data = "\n".join(histo1dbin_to_str(b) for b in histo.bins())

    footer = "END YODA_HISTO1D_V2\n"

    return f"{header}{stats}{underflow}\n{overflow}\n# xlow\t xhigh\t sumw\t sumw2\t sumwx\t sumwx2\t numEntries\n{bin_data}\n{footer}"
