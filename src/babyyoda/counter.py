import contextlib

import numpy as np


def set_bin0d(target, source):
    if hasattr(target, "set"):
        target.set(
            source.numEntries(),
            [source.sumW()],
            [source.sumW2()],
        )
    else:
        err = "YODA1 backend can not set bin values"
        raise NotImplementedError(err)


def Counter(*args, **kwargs):
    """
    Automatically select the correct version of the Histo1D class
    """
    try:
        from babyyoda import yoda
    except ImportError:
        import babyyoda.grogu as yoda
    return yoda.Counter(*args, **kwargs)


# TODO make this implementation independent (no V2 or V3...)
class UHICounter:
    ######
    # BACKENDS
    ######

    # def to_grogu_v2(self):
    #    from babyyoda.grogu.histo1d_v2 import GROGU_HISTO1D_V2

    #    return GROGU_HISTO1D_V2(
    #        d_key=self.key(),
    #        d_path=self.path(),
    #        d_title=self.title(),
    #        d_bins=[
    #            GROGU_HISTO1D_V2.Bin(
    #                d_xmin=self.xEdges()[i],
    #                d_xmax=self.xEdges()[i + 1],
    #                d_sumw=b.sumW(),
    #                d_sumw2=b.sumW2(),
    #                d_sumwx=b.sumWX(),
    #                d_sumwx2=b.sumWX2(),
    #                d_numentries=b.numEntries(),
    #            )
    #            for i, b in enumerate(self.bins())
    #        ],
    #        d_overflow=GROGU_HISTO1D_V2.Bin(
    #            d_xmin=None,
    #            d_xmax=None,
    #            d_sumw=self.overflow().sumW(),
    #            d_sumw2=self.overflow().sumW2(),
    #            d_sumwx=self.overflow().sumWX(),
    #            d_sumwx2=self.overflow().sumWX2(),
    #            d_numentries=self.overflow().numEntries(),
    #        ),
    #        d_underflow=GROGU_HISTO1D_V2.Bin(
    #            d_xmin=None,
    #            d_xmax=None,
    #            d_sumw=self.underflow().sumW(),
    #            d_sumw2=self.underflow().sumW2(),
    #            d_sumwx=self.underflow().sumWX(),
    #            d_sumwx2=self.underflow().sumWX2(),
    #            d_numentries=self.underflow().numEntries(),
    #        ),
    #    )

    # def to_grogu_v3(self):
    #    from babyyoda.grogu.histo1d_v3 import GROGU_HISTO1D_V3

    #    return GROGU_HISTO1D_V3(
    #        d_key=self.key(),
    #        d_path=self.path(),
    #        d_title=self.title(),
    #        d_edges=self.xEdges(),
    #        d_bins=[
    #            GROGU_HISTO1D_V3.Bin(
    #                d_sumw=self.underflow().sumW(),
    #                d_sumw2=self.underflow().sumW2(),
    #                d_sumwx=self.underflow().sumWX(),
    #                d_sumwx2=self.underflow().sumWX2(),
    #                d_numentries=self.underflow().numEntries(),
    #            )
    #        ]
    #        + [
    #            GROGU_HISTO1D_V3.Bin(
    #                d_sumw=b.sumW(),
    #                d_sumw2=b.sumW2(),
    #                d_sumwx=b.sumWX(),
    #                d_sumwx2=b.sumWX2(),
    #                d_numentries=b.numEntries(),
    #            )
    #            for b in self.bins()
    #        ]
    #        + [
    #            GROGU_HISTO1D_V3.Bin(
    #                d_sumw=self.overflow().sumW(),
    #                d_sumw2=self.overflow().sumW2(),
    #                d_sumwx=self.overflow().sumWX(),
    #                d_sumwx2=self.overflow().sumWX2(),
    #                d_numentries=self.overflow().numEntries(),
    #            )
    #        ],
    #    )

    # def to_yoda_v3(self):
    #    err = "Not implemented yet"
    #    raise NotImplementedError(err)

    # def to_string(self):
    #    # Now we need to map YODA to grogu and then call to_string
    #    # TODO do we want to hardcode v3 here?
    #    return self.to_grogu_v3().to_string()

    ########################################################
    # YODA compatibility code (dropped legacy code?)
    ########################################################

    def errWs(self):
        return np.sqrt(np.array([b.sumW2() for b in self.bins()]))

    def sumWs(self):
        return np.array([b.sumW() for b in self.bins()])

    def sumW2s(self):
        return np.array([b.sumW2() for b in self.bins()])

    def integral(self, includeOverflows=True):
        return sum(b.sumW() for b in self.bins(includeOverflows=includeOverflows))

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
        return np.array([b.numEntries() for b in self.bins()])

    def values(self):
        return np.array([b.sumW() for b in self.bins()])

    def variances(self):
        return np.array([(b.sumW2()) for b in self.bins()])

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
