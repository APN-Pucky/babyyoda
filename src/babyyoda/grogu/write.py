from babyyoda.util import open_write_file


def write(histograms, file_path: str, gz=False):
    """Write multiple histograms to a file in YODA format."""
    with open_write_file(file_path, gz=gz) as f:
        # if dict loop over values
        if isinstance(histograms, dict):
            histograms = histograms.values()
        for histo in histograms:
            f.write(histo.to_string())
            f.write("\n")
