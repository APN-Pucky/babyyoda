from babyyoda import grogu


def write(anyhistograms, file_path: str, *args, **kwargs):
    # if dict loop over values
    if isinstance(anyhistograms, dict):
        listhistograms = anyhistograms.values()
    # check if all histograms are yoda => use yoda
    use_yoda = True
    try:
        from babyyoda import yoda

        for h in listhistograms:
            if not (isinstance(h, (yoda.Histo1D, yoda.Histo2D))):
                use_yoda = False
                break
    except ImportError:
        use_yoda = False

    if use_yoda:
        write_yoda(anyhistograms, file_path, *args, **kwargs)
    else:
        write_grogu(anyhistograms, file_path, *args, **kwargs)


# These functions are just to be similar to the read functions
def write_grogu(histograms, file_path: str, gz=False):
    grogu.write(histograms, file_path, gz=gz)


def write_yoda(histograms, file_path: str, gz=False):
    # TODO we could force convert to YODA in Histo{1,2}D here ...
    from babyyoda import yoda

    yoda.write(histograms, file_path, gz=gz)
