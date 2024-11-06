import gzip
import re
from io import BufferedReader
from typing import Union

from babyyoda.grogu.counter_v2 import GROGU_COUNTER_V2
from babyyoda.grogu.counter_v3 import GROGU_COUNTER_V3
from babyyoda.grogu.histo1d_v2 import GROGU_HISTO1D_V2
from babyyoda.grogu.histo1d_v3 import GROGU_HISTO1D_V3
from babyyoda.grogu.histo2d_v2 import GROGU_HISTO2D_V2
from babyyoda.grogu.histo2d_v3 import GROGU_HISTO2D_V3


# Copied from pylhe
def _extract_fileobj(filepath: str) -> Union[gzip.GzipFile, BufferedReader]:
    """
    Checks to see if a file is compressed, and if so, extract it with gzip
    so that the uncompressed file can be returned.
    It returns a file object containing XML data that will be ingested by
    ``xml.etree.ElementTree.iterparse``.

    Args:
        filepath: A path-like object or str.

    Returns:
        _io.BufferedReader or gzip.GzipFile: A file object containing XML data.
    """
    with open(filepath, "rb") as gzip_file:
        header = gzip_file.read(2)
    gzip_magic_number = b"\x1f\x8b"

    return (
        gzip.GzipFile(filepath) if header == gzip_magic_number else open(filepath, "rb")
    )


Histograms = Union[
    GROGU_COUNTER_V2,
    GROGU_COUNTER_V3,
    GROGU_HISTO1D_V2,
    GROGU_HISTO1D_V3,
    GROGU_HISTO2D_V2,
    GROGU_HISTO2D_V3,
]


def read(
    file_path: str,
) -> dict[
    str,
    Histograms,
]:
    with _extract_fileobj(file_path) as f:
        bcontent = f.read()
        content = bcontent.decode("utf-8")
    pattern = re.compile(
        r"(BEGIN (YODA_[A-Z0-9_]+) ([^\n]+)\n(.*?)\nEND \2)", re.DOTALL
    )
    matches = pattern.findall(content)

    histograms: dict[str, Histograms] = {}

    for full_match, hist_type, name, _body in matches:
        if hist_type == "YODA_COUNTER_V2":
            histograms[name] = GROGU_COUNTER_V2.from_string(full_match)
        elif hist_type == "YODA_COUNTER_V3":
            histograms[name] = GROGU_COUNTER_V3.from_string(full_match)
        elif hist_type == "YODA_HISTO1D_V2":
            histograms[name] = GROGU_HISTO1D_V2.from_string(full_match)
        elif hist_type == "YODA_HISTO1D_V3":
            histograms[name] = GROGU_HISTO1D_V3.from_string(full_match)
        elif hist_type == "YODA_HISTO2D_V2":
            histograms[name] = GROGU_HISTO2D_V2.from_string(full_match)
        elif hist_type == "YODA_HISTO2D_V3":
            histograms[name] = GROGU_HISTO2D_V3.from_string(full_match)
        else:
            # Add other parsing logic for different types if necessary
            print(f"Unknown type: {hist_type}, skipping...")

    return histograms
