def write(histograms, file_path: str):
    """Write multiple histograms to a file in YODA format."""
    with open(file_path, "w") as f:
        # if dict loop over values
        if isinstance(histograms, dict):
            histograms = histograms.values()
        for histo in histograms:
            f.write(histo.to_string())
            f.write("\n")
