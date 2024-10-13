import gzip


def open_file(file_path, gz=False):
    if file_path.endswith(".gz") or file_path.endswith(".gzip") or gz:
        return gzip.open(file_path, "wt")
    else:
        return open(file_path, "w")


def write(histograms, file_path: str, gz=False):
    """Write multiple histograms to a file in YODA format."""
    with open_file(file_path, gz=gz) as f:
        # if dict loop over values
        if isinstance(histograms, dict):
            histograms = histograms.values()
        for histo in histograms:
            f.write(histo.to_string())
            f.write("\n")
