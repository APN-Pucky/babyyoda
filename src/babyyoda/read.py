from typing import Any

from babyyoda import grogu


def read(file_path: str) -> dict[str, Any]:
    try:
        return read_yoda(file_path)
    except ImportError:
        # warnings.warn(
        #    "yoda is not installed, falling back to python grogu implementation",
        #    stacklevel=2,
        # )
        return read_grogu(file_path)


def read_yoda(file_path: str) -> dict[str, Any]:
    """
    Wrap yoda histograms in the yoda classes
    """
    from babyyoda import yoda

    return yoda.read(file_path)


def read_grogu(file_path: str) -> dict[str, Any]:
    """
    Wrap grogu histograms in the by classes
    """
    return grogu.read(file_path)
