from babyyoda import yoda as baby_yoda


def read(file_path: str):
    """
    Wrap yoda histograms in the by HISTO1D_V2 class
    """
    import yoda as yd

    ret = {}
    for k, v in yd.read(file_path).items():
        if isinstance(v, yd.Histo1D):
            ret[k] = baby_yoda.Histo1D(v)
        elif isinstance(v, yd.Histo2D):
            ret[k] = baby_yoda.Histo2D(v)
        else:
            ret[k] = v
    return ret
