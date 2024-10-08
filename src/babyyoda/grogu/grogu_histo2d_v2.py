import re
from dataclasses import dataclass

@dataclass
class GROGU_HISTO2D_V2:
    @dataclass
    class Bin:
        xmin : float
        xmax : float
        ymin : float
        ymax : float
        sumw : float
        sumw2 : float
        sumwx : float
        sumwx2 : float
        sumwy : float
        sumwy2 : float
        sumwxy : float
        numentries : float

        ########################################################
        # YODA compatibilty code
        ########################################################

        def xMin(self):
            return self.xmin
        
        def xMax(self):
            return self.xmax

        def yMin(self):
            return self.ymin
        
        def yMax(self):
            return self.ymax

        def sumW(self):
            return self.sumw

        def sumW2(self):
            return self.sumw2

        def numEntries(self):
            return self.numentries





    name: str
    path: str
    title: str
    path: str
    entries : list[Bin]
    #_bins: list[Bin]
    overflow : Bin
    underflow : Bin

    type: str = "Histo2D"

    #
    # YODA compatibilty code
    #

    def bins(self):
        # sort the bins by xlow, then ylow
        return sorted(self.entries, key=lambda b: (b.ymin, b.xmin))

def parse_histo2d_v2(file_content:str, name :str = "") -> GROGU_HISTO2D_V2:
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
            underflow = GROGU_HISTO2D_V2.Bin(None, None, None, None, float(values[2]), float(values[3]), float(values[4]), float(values[5]), float(values[6]), float(values[7]), float(values[8]), float(values[9]))
        elif values[0] == "Overflow":
            overflow = GROGU_HISTO2D_V2.Bin(None, None, None, None, float(values[2]), float(values[3]), float(values[4]), float(values[5]), float(values[6]), float(values[7]), float(values[8]), float(values[9]))
        elif values[0] == "Total":
            pass
        else:
            xlow, xhigh, ylow, yhigh, sumw, sumw2, sumwx, sumwx2, sumwy, sumwy2, sumwxy, numEntries = map(float, values)
            bins.append(GROGU_HISTO2D_V2.Bin(xlow, xhigh, ylow, yhigh, sumw, sumw2, sumwx, sumwx2, sumwy, sumwy2, sumwxy, numEntries))

    return GROGU_HISTO2D_V2(
        name=name,
        path=path,
        title=title,
        entries=bins,
        underflow=underflow,
        overflow=overflow
    )




