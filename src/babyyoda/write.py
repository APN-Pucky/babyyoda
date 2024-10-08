from babyyoda.Histo1D import YODA_HISTO1D_V2, yoda_histo1d_to_str


def write(histograms:list[YODA_HISTO1D_V2], file_path: str):
    """Write multiple histograms to a file in YODA format."""
    with open(file_path, 'w') as f:
        for histo in histograms:
            f.write(yoda_histo1d_to_str(histo))