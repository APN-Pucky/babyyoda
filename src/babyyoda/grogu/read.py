import re

from babyyoda.grogu.histo1d_v2 import parse_histo1d_v2
from babyyoda.grogu.histo2d_v2 import parse_histo2d_v2


def read(file_path: str):
    with open(file_path) as f:
        content = f.read()

    pattern = re.compile(r"BEGIN (YODA_[A-Z0-9_]+) ([^\n]+)\n(.*?)\nEND \1", re.DOTALL)
    matches = pattern.findall(content)

    histograms = {}

    for hist_type, name, body in matches:
        if hist_type == "YODA_HISTO1D_V2":
            hist = parse_histo1d_v2(body, name)
            histograms[name] = hist
        elif hist_type == "YODA_HISTO2D_V2":
            hist = parse_histo2d_v2(body, name)
            histograms[name] = hist
        else:
            # Add other parsing logic for different types if necessary
            print(f"Unknown type: {hist_type}, skipping...")

    return histograms
