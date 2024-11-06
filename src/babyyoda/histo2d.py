import contextlib
import sys
from typing import Any, Optional, Union

import numpy as np

from babyyoda.analysisobject import UHIAnalysisObject
from babyyoda.histo1d import UHIHisto1D
from babyyoda.util import (
    loc,
    overflow,
    project,
    rebin,
    rebinBy_to_rebinTo,
    shift_rebinby,
    shift_rebinto,
    underflow,
)


def set_bin2d(target: Any, source: Any) -> None:
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


def Histo2D(*args: list[Any], **kwargs: list[Any]) -> "UHIHisto2D":
    """
    Automatically select the correct version of the Histo2D class
    """
    try:
        from babyyoda import yoda

        return yoda.Histo2D(*args, **kwargs)
    except ImportError:
        from babyyoda import grogu

        return grogu.Histo2D(*args, **kwargs)


class UHIHisto2D(UHIAnalysisObject):
    ######
    # Minimum required functions
    ######

    def bins(self, includeOverflows: bool = False) -> list[Any]:
        raise NotImplementedError

    def xEdges(self) -> list[float]:
        raise NotImplementedError

    def yEdges(self) -> list[float]:
        raise NotImplementedError

    def rebinXTo(self, edges: list[float]) -> None:
        raise NotImplementedError

    def rebinYTo(self, edges: list[float]) -> None:
        raise NotImplementedError

    def annotationsDict(self) -> dict[str, Optional[str]]:
        raise NotImplementedError

    def clone(self) -> "UHIHisto2D":
        raise NotImplementedError

    def get_projector(self) -> type[UHIHisto1D]:
        raise NotImplementedError

    #####
    # BACKENDS
    #####

    def to_grogu_v2(self) -> Any:
        from babyyoda.grogu.histo2d_v2 import GROGU_HISTO2D_V2

        tot = GROGU_HISTO2D_V2.Bin()
        for b in self.bins():
            tot.d_sumw += b.sumW()
            tot.d_sumw2 += b.sumW2()
            tot.d_sumwx += b.sumWX()
            tot.d_sumwx2 += b.sumWX2()
            tot.d_sumwy += b.sumWY()
            tot.d_sumwy2 += b.sumWY2()
            tot.d_sumwxy += b.crossTerm(0, 1)
            tot.d_numentries += b.numEntries()

        return GROGU_HISTO2D_V2(
            d_key=self.key(),
            d_annotations=self.annotationsDict(),
            d_total=tot,
            d_bins=[
                GROGU_HISTO2D_V2.Bin(
                    d_xmin=self.xEdges()[i % (len(self.xEdges()) - 1)],
                    d_xmax=self.xEdges()[i % (len(self.xEdges()))],
                    d_ymin=self.yEdges()[i // (len(self.xEdges()) - 1)],
                    d_ymax=self.yEdges()[i // (len(self.xEdges()))],
                    d_sumw=b.sumW(),
                    d_sumw2=b.sumW2(),
                    d_sumwx=b.sumWX(),
                    d_sumwx2=b.sumWX2(),
                    d_sumwy=b.sumWY(),
                    d_sumwy2=b.sumWY2(),
                    d_sumwxy=b.crossTerm(0, 1),
                    d_numentries=b.numEntries(),
                )
                for i, b in enumerate(self.bins())
            ],
        )

    def to_grogu_v3(self) -> Any:
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

    def xMins(self) -> list[float]:
        return self.xEdges()[:-1]
        # return np.array(sorted(list(set([b.xMin() for b in self.bins()]))))

    def xMaxs(self) -> list[float]:
        return self.xEdges()[1:]
        # return np.array(sorted(list(set([b.xMax() for b in self.bins()]))))

    def yMins(self) -> list[float]:
        return self.yEdges()[:-1]
        # return np.array(sorted(list(set([b.yMin() for b in self.bins()]))))

    def yMaxs(self) -> list[float]:
        return self.yEdges()[1:]
        # return np.array(sorted(list(set([b.yMax() for b in self.bins()]))))

    def sumWs(self) -> list[float]:
        return [b.sumW() for b in self.bins()]

    def sumWXYs(self) -> list[float]:
        return [b.crossTerm(0, 1) for b in self.bins()]

    def xMean(self, includeOverflows: bool = True) -> float:
        return sum(
            float(b.sumWX()) for b in self.bins(includeOverflows=includeOverflows)
        ) / sum(float(b.sumW()) for b in self.bins(includeOverflows=includeOverflows))

    def yMean(self, includeOverflows: bool = True) -> float:
        return sum(
            float(b.sumWY()) for b in self.bins(includeOverflows=includeOverflows)
        ) / sum(float(b.sumW()) for b in self.bins(includeOverflows=includeOverflows))

    def integral(self, includeOverflows: bool = True) -> float:
        return sum(
            float(b.sumW()) for b in self.bins(includeOverflows=includeOverflows)
        )

    def rebinXBy(self, factor: int, begin: int = 1, end: int = sys.maxsize) -> None:
        new_edges = rebinBy_to_rebinTo(self.xEdges(), factor, begin, end)
        self.rebinXTo(new_edges)

    def rebinYBy(self, factor: int, begin: int = 1, end: int = sys.maxsize) -> None:
        new_edges = rebinBy_to_rebinTo(self.yEdges(), factor, begin, end)
        self.rebinYTo(new_edges)

    def dVols(self) -> list[float]:
        ret = []
        for iy in range(len(self.yMins())):
            for ix in range(len(self.xMins())):
                ret.append(
                    (self.xMaxs()[ix] - self.xMins()[ix])
                    * (self.yMaxs()[iy] - self.yMins()[iy])
                )
        return ret

    ########################################################
    # Generic UHI code
    ########################################################

    @property
    def axes(self) -> list[list[tuple[float, float]]]:
        return [
            list(zip(self.xMins(), self.xMaxs())),
            list(zip(self.yMins(), self.yMaxs())),
        ]

    @property
    def kind(self) -> str:
        # TODO reeavaluate this
        return "COUNT"

    def values(self) -> np.ndarray:
        return np.array(self.sumWs()).reshape((len(self.axes[1]), len(self.axes[0]))).T

    def variances(self) -> np.ndarray:
        return (
            np.array([b.sumW2() for b in self.bins()])
            .reshape((len(self.axes[1]), len(self.axes[0])))
            .T
        )

    def counts(self) -> np.ndarray:
        return (
            np.array([b.numEntries() for b in self.bins()])
            .reshape((len(self.axes[1]), len(self.axes[0])))
            .T
        )

    def __single_index(self, ix: int, iy: int) -> int:
        return iy * len(self.axes[0]) + ix
        # return ix * len(self.axes[1]) + iy

    def __get_by_indices(self, ix: int, iy: int) -> Any:
        return self.bins()[
            self.__single_index(ix, iy)
        ]  # THIS is the fault with/without overflows!

    def __get_index_by_loc(self, oloc: loc, bins: list[tuple[float, float]]) -> int:
        # find the index in bin where loc is
        for a, b in bins:
            if a <= oloc.value and oloc.value < b:
                return bins.index((a, b)) + oloc.offset
        err = f"loc {oloc.value} is not in the range of {bins}"
        raise ValueError(err)

    def __get_x_index(self, slices: Union[int, loc]) -> Optional[int]:
        ix = None
        if isinstance(slices, int):
            ix = slices
        if isinstance(slices, loc):
            ix = self.__get_index_by_loc(slices, self.axes[0])
        return ix

    def __get_y_index(self, slices: Union[int, loc]) -> Optional[int]:
        iy = None
        if isinstance(slices, int):
            iy = slices
        if isinstance(slices, loc):
            iy = self.__get_index_by_loc(slices, self.axes[1])
        return iy

    def __get_indices(
        self, slices: tuple[Union[int, loc], Union[int, loc]]
    ) -> tuple[Optional[int], Optional[int]]:
        return self.__get_x_index(slices[0]), self.__get_y_index(slices[1])

    def __setitem__(
        self, slices: tuple[Union[int, slice, loc], Union[int, slice, loc]], value: Any
    ) -> None:
        set_bin2d(self.__getitem__(slices), value)

    def __getitem__(
        self, slices: tuple[Union[int, slice, loc], Union[int, slice, loc]]
    ) -> Any:
        # integer index
        if slices is underflow:  # type: ignore[comparison-overlap]
            err = "No underflow bin in 2D histogram"
            raise TypeError(err)
        if slices is overflow:  # type: ignore[comparison-overlap]
            err = "No overflow bin in 2D histogram"
            raise TypeError(err)
        if isinstance(slices, tuple) and len(slices) == 2:  # type: ignore[redundant-expr]
            ix, iy = self.__get_indices(slices)
            if isinstance(ix, int) and isinstance(iy, int):
                return self.__get_by_indices(ix, iy)
            if isinstance(slices[0], slice) and isinstance(iy, int):
                slices = (slices[0], slice(iy, iy + 1, project))
            if isinstance(ix, int) and isinstance(slices[1], slice):
                slices = (slice(ix, ix + 1, project), slices[1])
            s_ix, s_iy = slices
            sc = self.clone()
            if isinstance(s_ix, slice) and isinstance(s_iy, slice):
                xstart, xstop, xstep = (
                    self.__get_x_index(s_ix.start),
                    self.__get_x_index(s_ix.stop),
                    s_ix.step,
                )
                ystart, ystop, ystep = (
                    self.__get_y_index(s_iy.start),
                    self.__get_y_index(s_iy.stop),
                    s_iy.step,
                )

                if isinstance(ystep, rebin):
                    ystart, ystop = shift_rebinby(ystart, ystop)
                    sc.rebinYBy(ystep.factor, ystart, ystop)
                elif ystep is project:
                    ystart, ystop = shift_rebinto(ystart, ystop)
                    sc.rebinYTo(sc.yEdges()[ystart:ystop])
                    sc = sc.projectY()
                    # sc = sc[:, ystart:ystop].projectY()
                else:
                    ystart, ystop = shift_rebinto(ystart, ystop)
                    sc.rebinYTo(self.yEdges()[ystart:ystop])

                if isinstance(xstep, rebin):
                    # weird yoda default
                    xstart, xstop = shift_rebinby(xstart, xstop)
                    sc.rebinXBy(xstep.factor, xstart, xstop)
                elif xstep is project:
                    xstart, xstop = shift_rebinto(xstart, xstop)
                    sc.rebinXTo(sc.xEdges()[xstart:xstop])
                    # project defaults to projectX, but since we might have already projected Y
                    # we use the generic project that also exists for 1D
                    sc = sc.project()
                else:
                    xstart, xstop = shift_rebinto(xstart, xstop)
                    sc.rebinXTo(self.xEdges()[xstart:xstop])

                return sc
            err = "Slice with Index not implemented"
            raise NotImplementedError(err)

        # TODO implement slice
        err = "Invalid argument type"
        raise TypeError(err)

    def projectX(self) -> Any:
        # Sum
        c = self.clone()
        c.rebinXTo([self.xEdges()[0], self.xEdges()[-1]])
        # pick
        p = self.get_projector()(self.yEdges())
        for pb, cb in zip(p.bins(), c.bins()):
            pb.set(cb.numEntries(), [cb.sumW(), cb.sumWY()], [cb.sumW2(), cb.sumWY2()])
        p.setAnnotationsDict(self.annotationsDict())
        return p

    def projectY(self) -> Any:
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
    def project(self, axis: int = 0) -> Any:
        assert axis in [0, 1]
        if axis == 0:
            return self.projectX()
        return self.projectY()

    def to_string(self) -> str:
        return str(self.to_grogu_v3().to_string())

    def plot(self, *args: Any, binwnorm: bool = True, **kwargs: Any) -> None:
        # # TODO should use histplot
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

            def temp_values() -> np.ndarray:
                return (
                    np.array(
                        [b.sumW() / vol for b, vol in zip(self.bins(), self.dVols())]
                    )
                    .reshape((len(self.axes[1]), len(self.axes[0])))
                    .T
                )

            self.values = temp_values  # type: ignore[method-assign]
        hep.hist2dplot(self, *args, **kwargs)
        if binwnorm:
            self.values = saved_values  # type: ignore[method-assign]

    def _ipython_display_(self) -> "UHIHisto2D":
        with contextlib.suppress(ImportError):
            self.plot()
        return self
