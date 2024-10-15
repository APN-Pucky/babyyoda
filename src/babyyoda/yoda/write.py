import warnings

import yoda as yd


def write(anyhistograms, file_path: str, *args, gz=False, **kwargs):
    if gz and not file_path.endswith((".gz", ".gzip")):
        warnings.warn(
            "gz is True but file_path does not end with .gz or .gzip", stacklevel=2
        )

    if isinstance(anyhistograms, dict):
        # replace every value of dict by value.target
        anyhistograms = {k: v.target for k, v in anyhistograms.items()}
        yd.write(anyhistograms, file_path, *args, **kwargs)
    elif isinstance(anyhistograms, list):
        # replace every value of list by value.target
        anyhistograms = [v.target for v in anyhistograms]
        yd.write(anyhistograms, file_path, *args, **kwargs)
    else:
        err = "anyhistograms should be a dict or a list of histograms"
        raise ValueError(err)
