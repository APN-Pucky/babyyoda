def write(anyhistograms, file_path: str, *args, **kwargs):
    import yoda as yd

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
