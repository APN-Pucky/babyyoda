from babyyoda import grogu
from babyyoda.util import is_yoda


def write(anyhistograms, file_path: str, *args, **kwargs):
    # if dict loop over values
    if isinstance(anyhistograms, dict):
        listhistograms = anyhistograms.values()
    # check if all histograms are yoda => use yoda
    use_yoda = True
    for h in listhistograms:
        if not is_yoda(h):
            use_yoda = False
            break
    if use_yoda:
        write_yoda(anyhistograms, file_path, *args, **kwargs)
    else:
        write_grogu(anyhistograms, file_path, *args, **kwargs)


# These functions are just to be similar to the read functions
def write_grogu(histograms, file_path: str, gz=False):
    grogu.write(histograms, file_path, gz=gz)


def write_yoda(histograms, file_path: str, gz=False):
    # TODO we could force convert to YODA in Histo{1,2}D here ...
    import yoda

    yoda.write(histograms, file_path, gz=gz)
