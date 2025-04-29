import warnings
from typing import Any, Union

import yoda as yd

import babyyoda.yoda as by

byHistograms = Union[by.Counter, by.Histo1D, by.Histo2D]
ydHistograms = Union[yd.Counter, yd.Histo1D, yd.Histo2D]
Histograms = Union[ydHistograms, byHistograms]


def write(
    anyhistograms: Union[list[Histograms], dict[str, Histograms]],
    file_path: str,
    *args: list[Any],
    gz: bool = False,
    **kwargs: dict[Any, Any],
) -> None:
    if gz and not file_path.endswith((".gz", ".gzip")):
        warnings.warn(
            "gz is True but file_path does not end with .gz or .gzip", stacklevel=2
        )

    if isinstance(anyhistograms, dict):
        # replace every value of dict by value.target
        tmpanyhistograms = {}
        for k,v in anyhistograms.items():
            if hasattr(v,"target"):
                tmpanyhistograms[k] = v.target
            else:
                tmpanyhistograms[k] = v
        yd.write(tmpanyhistograms, file_path, *args, **kwargs)
    elif isinstance(anyhistograms, list):
        # replace every value of list by value.target
        tmpanyhistograms = []
        for v in anyhistograms:
            if hasattr(v,"target"):
                tmpanyhistograms.append(v.target)
            else:
                tmpanyhistograms.append(v)
        yd.write(tmpanyhistograms, file_path, *args, **kwargs)
