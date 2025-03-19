from typing import Any, Union

import matplotlib.pyplot as plt

from babyyoda import read


def plot(file_or_dict: Union[str, dict[str, Any]]) -> None:
    """
    Plot the given file or dict
    """
    dic: dict[str, Any] = (
        read.read(file_or_dict) if isinstance(file_or_dict, str) else file_or_dict
    )

    for _, v in dic.items():
        if hasattr(v, "plot"):
            v.plot()
            plt.show()
