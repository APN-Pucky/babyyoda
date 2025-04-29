from typing import Any, List, Union

import matplotlib.pyplot as plt

from babyyoda import read


def plot(*files_or_dicts: List[Union[str, dict[str, Any]]]) -> None:
    """
    Plot the given file or dict
    """
    dics: List[dict[str, Any]] = [(
        read.read(file_or_dict) if isinstance(file_or_dict, str) else file_or_dict
    ) for file_or_dict in files_or_dicts]

    keys = set().union(*dics)

    for k in keys:
        for d in dics:
            if k not in d:
                continue
            v = d[k]
            if hasattr(v, "plot"):
                v.plot()
        plt.show()
