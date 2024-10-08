import re
from typing import Optional
from dataclasses import dataclass

@dataclass
class GROGU_HISTO1D_V2:
    @dataclass
    class Bin:
        xmin: Optional[float]
        xmax: Optional[float]
        sumw: float
        sumw2: float
        sumwx: float
        sumwx2: float
        numentries: float


        ########################################################
        # YODA compatibilty code
        ########################################################

        def xMin(self):
            return self.xmin

        def xMax(self):
            return self.xmax

        def sumW(self):
            return self.sumw

        def sumW2(self):
            return self.sumw2
    
        def sumWX(self):
            return self.sumwx
        
        def sumWX2(self):
            return self.sumwx2

        def numEntries(self):
            return self.numentries

        def __add__(self, other):
            nxhigh =None
            nxlow = None
            # combine if the bins are adjacent
            if self.xhigh == other.xlow:
                nxlow = self.xlow
                nxhigh = other.xhigh
            elif self.xlow == other.xhigh:
                nxlow = other.xlow
                nxhigh = self.xhigh
            return GROGU_HISTO1D_V2.Bin(
                nxlow,
                nxhigh,
                self.sumw + other.sumw,
                self.sumw2 + other.sumw2,
                self.sumwx + other.sumwx,
                self.sumwx2 + other.sumwx2,
                self.numEntries + other.numEntries,
            )

    name: str
    path: str
    title: str
    path: str
    entries : list[Bin]
    #_bins: list[Bin]
    overflow : Bin
    underflow : Bin
    type: str = "Histo1D"

    ########################################################
    # YODA compatibilty code
    ########################################################
    def bins(self):
        return self.entries

    def bin(self, *indices):
        return [self.bins()[i] for i in indices]

    def binAt(self, x):
        for b in self.bins():
            if b.xlow <= x < b.xhigh:
                return b
        return None

    def binDim(self):
        return 1


    def rebinBy(self, factor:int, start:None, stop:None):
        if start is None:
            start = 0
        if stop is None:
            stop = len(self.bins())
        new_bins = []
        for i in range(start, stop, factor):
            nb = self.bins[i]
            for j in range(1, factor):
                nb += self.bins[i+j]
            new_bins.append(nb)
        return GROGU_HISTO1D_V2(
            self.name,
            self.path,
            self.title,
            new_bins,
            self.underflow,
            self.overflow
        )

    def rebinTo(bins):
        raise NotImplementedError



def parse_histo1d_v2(file_content:str,name : str = "") -> GROGU_HISTO1D_V2:
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

        values = re.split(r'\s+', line.strip())
        if values[0] == "Underflow":
            underflow = GROGU_HISTO1D_V2.Bin(None, None, float(values[2]), float(values[3]), float(values[4]), float(values[5]), float(values[6]))
        elif values[0] == "Overflow":
            overflow = GROGU_HISTO1D_V2.Bin(None, None, float(values[2]), float(values[3]), float(values[4]), float(values[5]), float(values[6]))
        elif values[0] == "Total":
            # ignore for now
            pass
        else:
            # Regular bin
            xlow, xhigh, sumw, sumw2, sumwx, sumwx2, numEntries = map(float, values)
            bins.append(GROGU_HISTO1D_V2.Bin(xlow, xhigh, sumw, sumw2, sumwx, sumwx2, numEntries))

    # Create and return the YODA_HISTO1D_V2 object
    return GROGU_HISTO1D_V2(
        name=name,
        path=path,
        title=title,
        entries=bins,
        underflow=underflow,
        overflow=overflow
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
        f"BEGIN YODA_HISTO1D_V2 {histo.name}\n"
        f"Path: {histo.path}\n"
        f"Title: {histo.title}\n"
        f"Type: Histo1D\n"
        "---\n"
    )
    
    # Add the sumw and other info (we assume it's present in the metadata but you could also compute)
    stats = (
        f"# Mean: {sum(b.sumwx for b in histo.bins) / sum(b.sumw for b in histo.bins):.6e}\n"
        f"# Area: {sum(b.sumw for b in histo.bins):.6e}\n"
    )
    
    underflow = underflow_overflow_to_str(histo.underflow, "Underflow")
    overflow = underflow_overflow_to_str(histo.overflow, "Overflow")
    
    # Add the bin data
    bin_data = "\n".join(histo1dbin_to_str(b) for b in histo.bins)
    
    footer = "END YODA_HISTO1D_V2\n"
    
    return f"{header}{stats}{underflow}\n{overflow}\n# xlow\t xhigh\t sumw\t sumw2\t sumwx\t sumwx2\t numEntries\n{bin_data}\n{footer}"

