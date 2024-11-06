from typing import Any

from babyyoda import grogu


def write(anyhistograms: Any, file_path: str, *args: Any, **kwargs: Any) -> None:
    listhistograms: list[Any] = []
    # if dict loop over values
    if isinstance(anyhistograms, dict):
        listhistograms = list(anyhistograms.values())
    elif isinstance(anyhistograms, list):
        listhistograms = anyhistograms
    # check if all histograms are yoda => use yoda
    use_yoda = True
    try:
        from babyyoda import yoda

        for h in listhistograms:
            if not (isinstance(h, (yoda.Counter, yoda.Histo1D, yoda.Histo2D))):
                use_yoda = False
                break
    except ImportError:
        use_yoda = False

    if use_yoda:
        write_yoda(anyhistograms, file_path, *args, **kwargs)
    else:
        write_grogu(anyhistograms, file_path, *args, **kwargs)


# These functions are just to be similar to the read functions
def write_grogu(histograms: Any, file_path: str, gz: bool = False) -> None:
    grogu.write(histograms, file_path, gz=gz)


def write_yoda(histograms: Any, file_path: str, gz: bool = False) -> None:
    # TODO we could force convert to YODA in Histo{1,2}D here ...
    from babyyoda import yoda

    yoda.write(histograms, file_path, gz=gz)
