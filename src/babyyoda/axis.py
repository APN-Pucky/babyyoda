from collections.abc import Iterator

from uhi.typing.plottable import PlottableAxisGeneric, PlottableTraits


class UHITraits(PlottableTraits):
    @property
    def circular(self) -> bool:
        return False

    @property
    def discrete(self) -> bool:
        return False


class UHIAxis(PlottableAxisGeneric[tuple[float, float]]):
    @property
    def traits(self) -> UHITraits:
        return UHITraits()

    def __init__(self, values: list[tuple[float, float]]):
        self.values = values

    # access axis[i]
    def __getitem__(self, i: int) -> tuple[float, float]:
        return self.values[i]

    def __len__(self) -> int:
        return len(self.values)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UHIAxis):
            return self.values == other.values  # noqa: PD011
        return False

    def __iter__(self) -> Iterator[tuple[float, float]]:
        return iter(self.values)

    def index(self, value: tuple[float, float]) -> int:
        return self.values.index(value)
