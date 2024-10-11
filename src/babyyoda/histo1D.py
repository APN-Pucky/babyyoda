import sys
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
    def __init__(self, *args, backend=None, **kwargs):
        """
        target is either a yoda or grogu HISTO1D_V2
        """
        if len(args) == 1:
            target = args[0]
            # Store the target object where calls and attributes will be forwarded
        else:
            # Pick faster backend if possible
            if backend is None:
                try:
                    import yoda

                    backend = yoda.Histo1D
                except ImportError:
                    backend = babyyoda.grogu.Histo1D_v3
            target = backend(*args, **kwargs)

        # unwrap target
        while isinstance(target, Histo1D):
            target = target.target

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
        return self.xEdges()[:-1]
        # return np.array([b.xMin() for b in self.bins()])

    def xMaxs(self):
        return self.xEdges()[1:]
        # return np.array([b.xMax() for b in self.bins()])

    def sumWs(self):
        return np.array([b.sumW() for b in self.bins()])

    def sumW2s(self):
        return np.array([b.sumW2() for b in self.bins()])

    def rebinXBy(self, factor: int, begin=1, end=sys.maxsize):
        if hasattr(self.target, "rebinXBy"):
            self.target.rebinXBy(factor, begin, end)
        else:
            # Just compute the new edges and call rebinXTo
            start = begin - 1
            stop = end
            if start is None:
                start = 0
            if stop >= sys.maxsize:
                stop = len(self.bins())
            else:
                stop = stop - 1
            new_edges = []
            # new_bins = []
            # new_bins += [self.underflow()]
            for i in range(0, start):
                # new_bins.append(self.bins()[i].clone())
                new_edges.append(self.xEdges()[i])
                new_edges.append(self.xEdges()[i + 1])
            last = None
            for i in range(start, stop, factor):
                if i + factor <= len(self.bins()):
                    xmin = self.xEdges()[i]
                    xmax = self.xEdges()[i + 1]
                    # nb = GROGU_HISTO1D_V3.Bin()
                    for j in range(0, factor):
                        last = i + j
                        # nb += self.bins()[i + j]
                        xmin = min(xmin, self.xEdges()[i + j])
                        xmax = max(xmax, self.xEdges()[i + j + 1])
                    # new_bins.append(nb)
                    # add both edges
                    new_edges.append(xmin)
                    new_edges.append(xmax)
            for j in range(last + 1, len(self.bins())):
                # new_bins.append(self.bins()[j].clone())
                new_edges.append(self.xEdges()[j])
                new_edges.append(self.xEdges()[j + 1])
            # new_bins += [self.overflow()]
            # self.d_bins = new_bins
            # drop duplicate edges
            self.rebinXTo(list(set(new_edges)))
            return

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

            sc = self.clone()
            if isinstance(step, rebin):
                # weird yoda default
                if start is None:
                    start = 1
                else:
                    start += 1
                if stop is None:
                    stop = sys.maxsize
                else:
                    stop += 1
                sc.rebinBy(step.factor, start, stop)
            else:
                if stop is not None:
                    stop += 1
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
            self,
            *args,
            yerr=self.variances() ** 0.5,
            w2method="sqrt",
            binwnorm=binwnorm,
            **kwargs,
        )

    def _ipython_display_(self):
        try:
            self.plot()
        except ImportError:
            pass
        return self
