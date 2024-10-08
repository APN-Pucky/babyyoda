import re
import warnings

from babyyoda.Histo1D import HISTO1D_V2
from babyyoda.Histo2D import HISTO2D_V2
from babyyoda.grogu.grogu_histo1d_v2 import parse_histo1d_v2
from babyyoda.grogu.grogu_histo2d_v2 import parse_histo2d_v2


def read(file_path:str):
    try:
        return read_yoda(file_path)
    except ImportError:
        warnings.warn("yoda is not installed, falling back to python grogu implementation")
        return read_grogu(file_path)

def read_yoda(file_path:str):
    """
    Wrap yoda histograms in the grogu HISTO1D_V2 class
    """
    import yoda as yd
    ret = {}
    for k,v in yd.read(file_path).items():
        if isinstance(v,yd.Histo1D):
            ret[k] = HISTO1D_V2(v)
        elif isinstance(v,yd.Histo2D):
            ret[k] = HISTO2D_V2(v)
        else:
            ret[k] = v
    return ret


def read_grogu(file_path:str):
    with open(file_path) as f:
        content = f.read()

    pattern = re.compile(r"BEGIN (YODA_[A-Z0-9_]+) ([^\n]+)\n(.*?)\nEND \1", re.DOTALL)
    matches = pattern.findall(content)

    histograms = {}

    for hist_type, name, body in matches:
        if hist_type == "YODA_HISTO1D_V2":
            hist = parse_histo1d_v2(body,name)
            histograms[name] = HISTO1D_V2(hist)
        elif hist_type == "YODA_HISTO2D_V2":
            hist = parse_histo2d_v2(body,name)
            histograms[name] = HISTO2D_V2(hist)
        else:
            # Add other parsing logic for different types if necessary
            print(f"Unknown type: {hist_type}, skipping...")

    return histograms