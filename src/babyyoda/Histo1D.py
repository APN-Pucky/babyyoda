import numpy as np
from babyyoda.util import loc, overflow, rebin, underflow


class HISTO1D_V2:
    def __init__(self, target):
        """
        target is either a yoda or grogu HISTO1D_V2
        """
        # Store the target object where calls and attributes will be forwarded
        super().__setattr__("target", target)

    ########################################################
    # Relay all attribute access to the target object
    ########################################################

    def __getattr__(self, name):
        # First, check if the Forwarder object itself has the attribute
        if name in self.__dict__ or hasattr(type(self), name):
            return object.__getattribute__(self, name)
        # If not, forward attribute access to the target
        elif hasattr(self.target, name):
            return getattr(self.target, name)
        raise AttributeError(
            f"'{type(self).__name__}' object and target have no attribute '{name}'"
        )

    def __setattr__(self, name, value):
        # First, check if the attribute belongs to the Forwarder itself
        if name in self.__dict__ or hasattr(type(self), name):
            object.__setattr__(self, name, value)
        # If not, forward attribute setting to the target
        elif hasattr(self.target, name):
            setattr(self.target, name, value)
        else:
            raise AttributeError(
                f"Cannot set attribute '{name}'; it does not exist in target or Forwarder."
            )

    def __call__(self, *args, **kwargs):
        # If the target is callable, forward the call, otherwise raise an error
        if callable(self.target):
            return self.target(*args, **kwargs)
        raise TypeError(f"'{type(self.target).__name__}' object is not callable")

    ########################################################
    # YODA compatibility code (dropped legacy code?)
    ########################################################

    def xMins(self):
        return np.array([b.xMin() for b in self.bins()])

    def xMaxs(self):
        return np.array([b.xMax() for b in self.bins()])

    def sumWs(self):
        return np.array([b.sumW() for b in self.bins()])

    ########################################################
    # Generic UHI code
    ########################################################

    @property
    def axes(self):
        return [list(zip(self.xMins(), self.xMaxs()))]

    @property
    def kind(self):
        return "COUNT"

    def counts(self):
        return np.array([b.numEntries() for b in self.bins()])

    def values(self):
        return np.array([b.sumW() for b in self.bins()])

    def variances(self):
        return np.array([b.sumW2() for b in self.bins()])

    def __setitem__(self, slices, value):
        # integer index
        index = self.__get_index(slices)
        self.__set_by_index(index, value)

    def __set_by_index(self, index, value):
        if index == underflow:
            self.underflow = value
            return
        if index == overflow:
            self.overflow = value
            return
        self.bins()[index] = value

    def __getitem__(self, slices):
        index = self.__get_index(slices)
        # integer index
        if isinstance(slices, int):
            return self.bins()[index]
        if isinstance(slices, loc):
            return self.bins()[index]
        if slices is underflow:
            return self.underflow()
        if slices is overflow:
            return self.overflow()

        if isinstance(slices, slice):
            # TODO handle ellipsis
            item = slices
            # print(f"slice {item}")
            start, stop, step = (
                self.__get_index(item.start),
                self.__get_index(item.stop),
                item.step,
            )
            if isinstance(step, rebin):
                if start is None:
                    start = 0
                return self.rebinBy(step.factor, start, stop)

            # print(f" {start} {stop} {step}")

            return self.rebinTo(self.bins()[start:stop])

        raise TypeError("Invalid argument type")

    def __get_index(self, slices):
        index = None
        if isinstance(slices, int):
            index = slices
            while index < 0:
                index = len(self.bins) + index
        if isinstance(slices, loc):
            # TODO cyclic maybe
            idx = None
            for i, b in enumerate(self.bins()):
                if slices.value >= b.xMin() and slices.value < b.xMax():
                    idx = i
            index = idx + slices.offset
        if slices is underflow:
            index = underflow
        if slices is overflow:
            index = overflow
        return index

    def plot(self, *args, w2method="sqrt", **kwargs):
        import mplhep as hep

        hep.histplot(self, w2=self.variances(), *args, w2method=w2method, **kwargs)

    def _ipython_display_(self):
        try:
            self.plot()
        except ImportError:
            pass
        return self
