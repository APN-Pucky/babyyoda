import numpy as np
import babyyoda
from babyyoda.util import loc, overflow, rebin, underflow


def set_bin(target, source):
    # TODO allow modify those?
    # self.d_xmin = bin.xMin()
    # self.d_xmax = bin.xMax()
    if hasattr(target, "set"):
        target.set(
            source.numEntries(),
            [source.sumW(), source.sumWX()],
            [source.sumW2(), source.sumWX2()],
        )
    else:
        raise NotImplementedError("YODA1 backend can not set bin values")


# TODO make this implementation independent (no V2 or V3...)
class Histo1D:
    def __init__(self, *args, backend=babyyoda.grogu.Histo1D_v3, **kwargs):
        """
        target is either a yoda or grogu HISTO1D_V2
        """
        if len(args) == 1:
            target = args[0]
            # Store the target object where calls and attributes will be forwarded
        else:
            target = backend(*args, **kwargs)
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

    # TODO __eq__ from test here?

    ########################################################
    # YODA compatibility code (dropped legacy code?)
    ########################################################

    def clone(self):
        return Histo1D(self.target.clone())

    def overflow(self):
        # if target has overflow method, call it
        if hasattr(self.target, "overflow"):
            return self.target.overflow()
        return self.bins(includeOverflows=True)[-1]

    def underflow(self):
        # if target has underflow method, call it
        if hasattr(self.target, "underflow"):
            return self.target.underflow()
        return self.bins(includeOverflows=True)[0]

    def errWs(self):
        return np.sqrt(np.array([b.sumW2() for b in self.bins()]))

    def xMins(self):
        return np.array([b.xMin() for b in self.bins()])

    def xMaxs(self):
        return np.array([b.xMax() for b in self.bins()])

    def sumWs(self):
        return np.array([b.sumW() for b in self.bins()])

    def sumW2s(self):
        return np.array([b.sumW2() for b in self.bins()])

    def rebinBy(self, *args, **kwargs):
        self.rebinXBy(*args, **kwargs)

    def rebinTo(self, *args, **kwargs):
        self.rebinXTo(*args, **kwargs)

    ########################################################
    # Generic UHI code
    ########################################################

    @property
    def axes(self):
        return [list(zip(self.xMins(), self.xMaxs()))]

    @property
    def kind(self):
        return "MEAN"

    def counts(self):
        return np.array([b.numEntries() for b in self.bins()])

    def values(self):
        return np.array([b.sumW() for b in self.bins()])

    def variances(self):
        return np.array([(b.sumW2()) for b in self.bins()])

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
                cs = self.clone()
                cs.rebinBy(step.factor, start, stop)
                return cs

            print(f" {start} {stop} {step}")
            if stop is not None:
                stop += 1
            sc = self.clone()
            sc.rebinTo(self.xEdges()[start:stop])
            return sc

        raise TypeError("Invalid argument type")

    def __get_index(self, slices):
        index = None
        if isinstance(slices, int):
            index = slices
            while index < 0:
                index = len(self.bins()) + index
        if isinstance(slices, loc):
            # TODO cyclic maybe
            idx = None
            for i, b in enumerate(self.bins()):
                if (
                    slices.value >= self.xEdges()[i]
                    and slices.value < self.xEdges()[i + 1]
                ):
                    idx = i
            index = idx + slices.offset
        if slices is underflow:
            index = underflow
        if slices is overflow:
            index = overflow
        return index

    def __set_by_index(self, index, value):
        if index == underflow:
            set_bin(self.underflow(), value)
            return
        if index == overflow:
            set_bin(self.overflow(), value)
            return
        set_bin(self.bins()[index], value)

    def __setitem__(self, slices, value):
        # integer index
        index = self.__get_index(slices)
        self.__set_by_index(index, value)

    def plot(self, *args, binwnorm=1.0, **kwargs):
        import mplhep as hep

        hep.histplot(
            self, *args, yerr=self.variances() ** 0.5, binwnorm=binwnorm, **kwargs
        )

    def _ipython_display_(self):
        try:
            self.plot()
        except ImportError:
            pass
        return self
