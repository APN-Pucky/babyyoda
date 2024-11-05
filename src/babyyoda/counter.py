import contextlib
from typing import Any, Optional

from babyyoda.analysisobject import UHIAnalysisObject


def set_bin0d(target: Any, source: Any) -> None:
    if hasattr(target, "set"):
        target.set(
            source.numEntries(),
            [source.sumW()],
            [source.sumW2()],
        )
    else:
        err = "YODA1 backend can not set bin values"
        raise NotImplementedError(err)


def Counter(*args, **kwargs) -> "UHICounter":
    """
    Automatically select the correct version of the Histo1D class
    """
    try:
        from babyyoda import yoda

        return yoda.Counter(*args, **kwargs)
    except ImportError:
        from babyyoda import grogu

        return grogu.Counter(*args, **kwargs)


# TODO make this implementation independent (no V2 or V3...)
class UHICounter(UHIAnalysisObject):
    ######
    # Minimum required functions
    ######

    def sumW(self) -> float:
        raise NotImplementedError

    def sumW2(self) -> float:
        raise NotImplementedError

    def numEntries(self) -> float:
        raise NotImplementedError

    def annotationsDict(self) -> dict[str, Optional[str]]:
        raise NotImplementedError

    def clone(self) -> "UHICounter":
        raise NotImplementedError

    ######
    # BACKENDS
    ######

    def to_grogu_v2(self) -> Any:
        from babyyoda.grogu.counter_v2 import GROGU_COUNTER_V2

        return GROGU_COUNTER_V2(
            d_key=self.key(),
            d_annotations=self.annotationsDict(),
            d_bins=[
                GROGU_COUNTER_V2.Bin(
                    d_sumw=self.sumW(),
                    d_sumw2=self.sumW2(),
                    d_numentries=self.numEntries(),
                )
            ],
        )

    def to_grogu_v3(self) -> Any:
        from babyyoda.grogu.counter_v3 import GROGU_COUNTER_V3

        return GROGU_COUNTER_V3(
            d_key=self.key(),
            d_annotations=self.annotationsDict(),
            d_bins=[
                GROGU_COUNTER_V3.Bin(
                    d_sumw=self.sumW(),
                    d_sumw2=self.sumW2(),
                    d_numentries=self.numEntries(),
                )
            ],
        )

    def to_yoda_v3(self) -> Any:
        err = "Not implemented yet"
        raise NotImplementedError(err)

    def to_string(self) -> str:
        # Now we need to map YODA to grogu and then call to_string
        # TODO do we want to hardcode v3 here?
        return self.to_grogu_v3().to_string()

    ########################################################
    # YODA compatibility code (dropped legacy code?)
    ########################################################

    ########################################################
    # Generic UHI code
    ########################################################

    @property
    def axes(self):
        return []

    @property
    def kind(self):
        # TODO reeavaluate this
        return "COUNT"

    def counts(self):
        return self.numEntries()

    def values(self):
        return self.sumW()

    def variances(self):
        return self.sumW2()

    def plot(self, *args, **kwargs):
        # TODO check UHI 0D plottable and mplhep hist plot 0D
        import matplotlib.pyplot as plt

        # Sample data
        # This is after Projections and we nolonger divide by bin width!?!?
        y = [self.values()]
        yerr = [self.variances() ** 0.5]

        # Plotting
        plt.errorbar(
            *args, x=[0] * len(y), y=y, yerr=yerr, fmt="o", capsize=5, **kwargs
        )
        # Remove x-axis labels and ticks
        plt.gca().get_xaxis().set_visible(False)
        # Show the plot
        # plt.show()

    def _ipython_display_(self):
        with contextlib.suppress(ImportError):
            self.plot()
        return self
