import contextlib
import sys

import numpy as np

from babyyoda.util import loc, overflow, rebin, underflow


def set_bin1d(target, source):
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
        err = "YODA1 backend can not set bin values"
        raise NotImplementedError(err)


def Histo1D(*args, **kwargs):
    """
    Automatically select the correct version of the Histo1D class
    """
    try:
        from babyyoda import yoda
    except ImportError:
        import babyyoda.grogu as yoda
    return yoda.Histo1D(*args, **kwargs)


# TODO make this implementation independent (no V2 or V3...)
class UHIHisto1D:
    ######
    # BACKENDS
    ######

    def to_grogu_v2(self):
        from babyyoda.grogu.histo1d_v2 import GROGU_HISTO1D_V2

        return GROGU_HISTO1D_V2(
            d_key=self.key(),
            d_path=self.path(),
            d_title=self.title(),
            d_bins=[
                GROGU_HISTO1D_V2.Bin(
                    d_xmin=self.xEdges()[i],
                    d_xmax=self.xEdges()[i + 1],
                    d_sumw=b.sumW(),
                    d_sumw2=b.sumW2(),
                    d_sumwx=b.sumWX(),
                    d_sumwx2=b.sumWX2(),
                    d_numentries=b.numEntries(),
                )
                for i, b in enumerate(self.bins())
            ],
            d_overflow=GROGU_HISTO1D_V2.Bin(
                d_xmin=None,
                d_xmax=None,
                d_sumw=self.overflow().sumW(),
                d_sumw2=self.overflow().sumW2(),
                d_sumwx=self.overflow().sumWX(),
                d_sumwx2=self.overflow().sumWX2(),
                d_numentries=self.overflow().numEntries(),
            ),
            d_underflow=GROGU_HISTO1D_V2.Bin(
                d_xmin=None,
                d_xmax=None,
                d_sumw=self.underflow().sumW(),
                d_sumw2=self.underflow().sumW2(),
                d_sumwx=self.underflow().sumWX(),
                d_sumwx2=self.underflow().sumWX2(),
                d_numentries=self.underflow().numEntries(),
            ),
        )

    def to_grogu_v3(self):
        from babyyoda.grogu.histo1d_v3 import GROGU_HISTO1D_V3

        return GROGU_HISTO1D_V3(
            d_key=self.key(),
            d_path=self.path(),
            d_title=self.title(),
            d_edges=self.xEdges(),
            d_bins=[
                GROGU_HISTO1D_V3.Bin(
                    d_sumw=self.underflow().sumW(),
                    d_sumw2=self.underflow().sumW2(),
                    d_sumwx=self.underflow().sumWX(),
                    d_sumwx2=self.underflow().sumWX2(),
                    d_numentries=self.underflow().numEntries(),
                )
            ]
            + [
                GROGU_HISTO1D_V3.Bin(
                    d_sumw=b.sumW(),
                    d_sumw2=b.sumW2(),
                    d_sumwx=b.sumWX(),
                    d_sumwx2=b.sumWX2(),
                    d_numentries=b.numEntries(),
                )
                for b in self.bins()
            ]
            + [
                GROGU_HISTO1D_V3.Bin(
                    d_sumw=self.overflow().sumW(),
                    d_sumw2=self.overflow().sumW2(),
                    d_sumwx=self.overflow().sumWX(),
                    d_sumwx2=self.overflow().sumWX2(),
                    d_numentries=self.overflow().numEntries(),
                )
            ],
        )

    def to_yoda_v3(self):
        err = "Not implemented yet"
        raise NotImplementedError(err)

    def to_string(self):
        # Now we need to map YODA to grogu and then call to_string
        # TODO do we want to hardcode v3 here?
        return self.to_grogu_v3().to_string()

    ########################################################
    # YODA compatibility code (dropped legacy code?)
    ########################################################

    def overflow(self):
        return self.bins(includeOverflows=True)[-1]

    def underflow(self):
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

    def xMean(self, includeOverflows=True):
        return sum(
            b.sumWX() for b in self.bins(includeOverflows=includeOverflows)
        ) / sum(b.sumW() for b in self.bins(includeOverflows=includeOverflows))

    def integral(self, includeOverflows=True):
        return sum(b.sumW() for b in self.bins(includeOverflows=includeOverflows))

    def rebinXBy(self, factor: int, begin=1, end=sys.maxsize):
        # Just compute the new edges and call rebinXTo
        start = begin - 1
        stop = end
        if start is None:
            start = 0
        stop = len(self.bins()) if stop >= sys.maxsize else stop - 1
        new_edges = []
        # new_bins = []
        # new_bins += [self.underflow()]
        for i in range(start):
            # new_bins.append(self.bins()[i].clone())
            new_edges.append(self.xEdges()[i])
            new_edges.append(self.xEdges()[i + 1])
        last = None
        for i in range(start, stop, factor):
            if i + factor <= len(self.bins()):
                xmin = self.xEdges()[i]
                xmax = self.xEdges()[i + 1]
                # nb = GROGU_HISTO1D_V3.Bin()
                for j in range(factor):
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
        # TODO reeavaluate this
        return "COUNT"

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

        err = "Invalid argument type"
        raise TypeError(err)

    def __get_index(self, slices):
        index = None
        if isinstance(slices, int):
            index = slices
            while index < 0:
                index = len(self.bins()) + index
        if isinstance(slices, loc):
            # TODO cyclic maybe
            idx = None
            for i, _b in enumerate(self.bins()):
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
            set_bin1d(self.underflow(), value)
            return
        if index == overflow:
            set_bin1d(self.overflow(), value)
            return
        set_bin1d(self.bins()[index], value)

    def __setitem__(self, slices, value):
        # integer index
        index = self.__get_index(slices)
        self.__set_by_index(index, value)

    def key(self):
        return self.path()

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
        with contextlib.suppress(ImportError):
            self.plot()
        return self
