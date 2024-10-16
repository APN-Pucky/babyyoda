import contextlib
import sys

import numpy as np

from babyyoda.analysisobject import UHIAnalysisObject
from babyyoda.util import loc, overflow, project, rebin, underflow


def set_bin2d(target, source):
    # TODO allow modify those?
    # self.d_xmin = bin.xMin()
    # self.d_xmax = bin.xMax()
    if hasattr(target, "set"):
        target.set(
            source.numEntries(),
            [source.sumW(), source.sumWX(), source.sumWY()],
            [source.sumW2(), source.sumWX2(), source.sumWY2()],
            [source.crossTerm(0, 1)],
        )
    else:
        err = "YODA1 backend can not set bin values"
        raise NotImplementedError(err)


def Histo2D(*args, **kwargs):
    """
    Automatically select the correct version of the Histo2D class
    """
    try:
        from babyyoda import yoda
    except ImportError:
        import babyyoda.grogu as yoda
    return yoda.Histo2D(*args, **kwargs)


class UHIHisto2D(UHIAnalysisObject):
    #####
    # BACKENDS
    #####

    def to_grogu_v2(self):
        from babyyoda.grogu.histo2d_v2 import GROGU_HISTO2D_V2

        return GROGU_HISTO2D_V2(
            d_key=self.key(),
            d_annotations=self.annotationsDict(),
            d_bins=[
                GROGU_HISTO2D_V2.Bin(
                    d_xmin=self.xEdges()[i % len(self.xEdges())],
                    d_xmax=self.xEdges()[i % len(self.xEdges()) + 1],
                    d_ymin=self.yEdges()[i // len(self.xEdges())],
                    d_ymax=self.yEdges()[i // len(self.xEdges()) + 1],
                    d_sumw=b.sumW(),
                    d_sumw2=b.sumW2(),
                    d_sumwx=b.sumWX(),
                    d_sumwx2=b.sumWX2(),
                    d_sumwy=b.sumWY(),
                    d_sumwy2=b.sumWY2(),
                    d_sumwxy=b.sumWXY(),
                    d_numentries=b.numEntries(),
                )
                for i, b in enumerate(self.bins())
            ],
        )

    def to_grogu_v3(self):
        from babyyoda.grogu.histo2d_v3 import GROGU_HISTO2D_V3

        bins = []
        try:
            bins = self.bins(True)
        except NotImplementedError:
            nobins = self.bins()
            bins += [GROGU_HISTO2D_V3.Bin()] * (len(self.xEdges()))
            for j in range(len(nobins)):
                if j % (len(self.xEdges()) - 1) == 0:
                    bins += [GROGU_HISTO2D_V3.Bin()]  # overflow
                    bins += [GROGU_HISTO2D_V3.Bin()]  # underflow
                bins += [nobins[j]]
            bins += [GROGU_HISTO2D_V3.Bin()]  # overflow
            bins += [GROGU_HISTO2D_V3.Bin()]  # underflow
            bins += [GROGU_HISTO2D_V3.Bin()] * (len(self.xEdges()))

        return GROGU_HISTO2D_V3(
            d_key=self.key(),
            d_annotations=self.annotationsDict(),
            d_edges=[self.xEdges(), self.yEdges()],
            d_bins=[
                GROGU_HISTO2D_V3.Bin(
                    d_sumw=b.sumW(),
                    d_sumw2=b.sumW2(),
                    d_sumwx=b.sumWX(),
                    d_sumwx2=b.sumWX2(),
                    d_sumwy=b.sumWY(),
                    d_sumwy2=b.sumWY2(),
                    d_sumwxy=b.crossTerm(0, 1),
                    d_numentries=b.numEntries(),
                )
                for b in bins
            ],
        )

    def to_string(self):
        if hasattr(self.target, "to_string"):
            return self.target.to_string()
        return self.to_grogu_v3().to_string()

    # def bins(self, *args, **kwargs):
    #    # fix order
    #    return self.target.bins(*args, **kwargs)
    #    return np.array(
    #        sorted(
    #            self.target.bins(*args, **kwargs), key=lambda b: (b.xMin(), b.yMin())
    #        )
    #    )

    # def bin(self, *indices):
    #    return self.bins()[indices]

    # def overflow(self):
    #    # This is a YODA-1 feature that is not present in YODA-2
    #    return self.bins(includeOverflows=True)[-1]

    # def underflow(self):
    #    # This is a YODA-1 feature that is not present in YODA-2
    #    return self.bins(includeOverflows=True)[0]

    def xMins(self):
        return self.xEdges()[:-1]
        # return np.array(sorted(list(set([b.xMin() for b in self.bins()]))))

    def xMaxs(self):
        return self.xEdges()[1:]
        # return np.array(sorted(list(set([b.xMax() for b in self.bins()]))))

    def yMins(self):
        return self.yEdges()[:-1]
        # return np.array(sorted(list(set([b.yMin() for b in self.bins()]))))

    def yMaxs(self):
        return self.yEdges()[1:]
        # return np.array(sorted(list(set([b.yMax() for b in self.bins()]))))

    def sumWs(self):
        return np.array([b.sumW() for b in self.bins()])

    def sumWXYs(self):
        return [b.crossTerm(0, 1) for b in self.bins()]

    def xMean(self, includeOverflows=True):
        return sum(b.sumWX() for b in self.d_bins) / sum(
            b.sumW() for b in self.bins(includeOverflows=includeOverflows)
        )

    def yMean(self, includeOverflows=True):
        return sum(b.sumWY() for b in self.d_bins) / sum(
            b.sumW() for b in self.bins(includeOverflows=includeOverflows)
        )

    def integral(self, includeOverflows=True):
        return sum(b.sumW() for b in self.bins(includeOverflows=includeOverflows))

    ########################################################
    # Generic UHI code
    ########################################################

    @property
    def axes(self):
        return [
            list(zip(self.xMins(), self.xMaxs())),
            list(zip(self.yMins(), self.yMaxs())),
        ]

    @property
    def kind(self):
        # TODO reeavaluate this
        return "COUNT"

    def values(self):
        return self.sumWs().reshape((len(self.axes[1]), len(self.axes[0]))).T

    def variances(self):
        return (
            np.array([b.sumW2() for b in self.bins()])
            .reshape((len(self.axes[1]), len(self.axes[0])))
            .T
        )

    def counts(self):
        return (
            np.array([b.numEntries() for b in self.bins()])
            .reshape((len(self.axes[1]), len(self.axes[0])))
            .T
        )

    def __single_index(self, ix, iy):
        return iy * len(self.axes[0]) + ix
        # return ix * len(self.axes[1]) + iy

    def __get_by_indices(self, ix, iy):
        return self.bins()[
            self.__single_index(ix, iy)
        ]  # THIS is the fault with/without overflows!

    def __get_index_by_loc(self, loc, bins):
        # find the index in bin where loc is
        for a, b in bins:
            if a <= loc.value and loc.value < b:
                return bins.index((a, b)) + loc.offset
        err = f"loc {loc.value} is not in the range of {bins}"
        raise ValueError(err)

    def __get_x_index(self, slices):
        ix = None
        if isinstance(slices, int):
            ix = slices
        if isinstance(slices, loc):
            ix = self.__get_index_by_loc(slices, self.axes[0])
        return ix

    def __get_y_index(self, slices):
        iy = None
        if isinstance(slices, int):
            iy = slices
        if isinstance(slices, loc):
            iy = self.__get_index_by_loc(slices, self.axes[1])
        return iy

    def __get_indices(self, slices):
        return self.__get_x_index(slices[0]), self.__get_y_index(slices[1])

    def __setitem__(self, slices, value):
        set_bin2d(self.__getitem__(slices), value)

    def __getitem__(self, slices):
        # integer index
        if slices is underflow:
            err = "No underflow bin in 2D histogram"
            raise TypeError(err)
        if slices is overflow:
            err = "No overflow bin in 2D histogram"
            raise TypeError(err)
        if isinstance(slices, tuple) and len(slices) == 2:
            ix, iy = self.__get_indices(slices)
            if isinstance(ix, int) and isinstance(iy, int):
                return self.__get_by_indices(ix, iy)
            if isinstance(slices[0], slice) and isinstance(iy, int):
                slices = (slices[0], slice(iy, iy + 1, project))
            if isinstance(ix, int) and isinstance(slices[1], slice):
                slices = (slice(ix, ix + 1, project), slices[1])
            ix, iy = slices
            sc = self.clone()
            if isinstance(ix, slice) and isinstance(iy, slice):
                xstart, xstop, xstep = (
                    self.__get_x_index(ix.start),
                    self.__get_x_index(ix.stop),
                    ix.step,
                )
                ystart, ystop, ystep = (
                    self.__get_y_index(iy.start),
                    self.__get_y_index(iy.stop),
                    iy.step,
                )

                if isinstance(ystep, rebin):
                    # weird yoda default
                    if ystart is None:
                        ystart = 1
                    else:
                        ystart += 1
                    if ystop is None:
                        ystop = sys.maxsize
                    else:
                        ystop += 1
                    sc.rebinYBy(ystep.factor, ystart, ystop)
                elif ystep is project:
                    sc = sc[:, ystart:ystop].projectY()
                else:
                    if ystop is not None:
                        ystop += 1
                    sc.rebinYTo(self.yEdges()[ystart:ystop])

                if isinstance(xstep, rebin):
                    # weird yoda default
                    if xstart is None:
                        xstart = 1
                    else:
                        xstart += 1
                    if xstop is None:
                        xstop = sys.maxsize
                    else:
                        xstop += 1
                    sc.rebinXBy(xstep.factor, xstart, xstop)
                elif xstep is project:
                    if xstop is not None:
                        xstop += 1
                    sc.rebinXTo(sc.xEdges()[xstart:xstop])
                    sc = sc.project()
                else:
                    if xstop is not None:
                        xstop += 1
                    sc.rebinXTo(self.xEdges()[xstart:xstop])

                return sc
            err = "Slice with Index not implemented"
            raise NotImplementedError(err)

        # TODO implement slice
        err = "Invalid argument type"
        raise TypeError(err)

    def projectX(self):
        # Sum
        c = self.clone()
        c.rebinXTo([self.xEdges()[0], self.xEdges()[-1]])
        # pick
        p = self.get_projector()(self.yEdges())
        for pb, cb in zip(p.bins(), c.bins()):
            pb.set(cb.numEntries(), [cb.sumW(), cb.sumWY()], [cb.sumW2(), cb.sumWY2()])
        p.setAnnotationsDict(self.annotationsDict())
        return p

    def projectY(self):
        # Sum
        c = self.clone()
        c.rebinYTo([self.yEdges()[0], self.yEdges()[-1]])
        # pick
        p = self.get_projector()(self.xEdges())
        for pb, cb in zip(p.bins(), c.bins()):
            pb.set(cb.numEntries(), [cb.sumW(), cb.sumWX()], [cb.sumW2(), cb.sumWX2()])
        p.setAnnotationsDict(self.annotationsDict())
        return p

    # TODO maybe N dim project
    def project(self, axis: int = 0):
        assert axis in [0, 1]
        if axis == 0:
            return self.projectX()
        return self.projectY()

    def plot(self, *args, binwnorm=True, **kwargs):
        ## TODO should use histplot
        # import mplhep as hep

        # hep.histplot(
        #    self,
        #    *args,
        #    #yerr=self.variances() ** 0.5,
        #    w2method="sqrt",
        #    binwnorm=binwnorm,
        #    **kwargs,
        # )
        import mplhep as hep

        if binwnorm:
            # Hack in the temporary division by dVol
            saved_values = self.values

            def temp_values():
                return (
                    np.array([b.sumW() / b.dVol() for b in self.bins()])
                    .reshape((len(self.axes[1]), len(self.axes[0])))
                    .T
                )

            self.values = temp_values
        hep.hist2dplot(self, *args, **kwargs)
        if binwnorm:
            self.values = saved_values

    def _ipython_display_(self):
        with contextlib.suppress(ImportError):
            self.plot()
        return self
