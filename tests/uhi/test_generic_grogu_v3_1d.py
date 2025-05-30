from __future__ import annotations

import uhi.testing.indexing

from babyyoda import grogu
from babyyoda.grogu.histo1d_v3 import GROGU_HISTO1D_V3
from babyyoda.histo1d import UHIHisto1D


class TestAccess1D(uhi.testing.indexing.Indexing1D[UHIHisto1D]):
    def bin_to_value(self, bin):
        return bin.sumW()

    def sum_to_value(self, bin):
        return bin.sumW()

    def value_to_bin(self, value):
        return GROGU_HISTO1D_V3.Bin(d_sumw=value)

    @staticmethod
    def make_histogram() -> UHIHisto1D:
        nbins = 10
        lower = 0
        upper = 1
        h = grogu.Histo1D(10, 0, 1, title="test")
        data = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        for i, d in enumerate(data):
            h.fill(lower - (lower - upper) / nbins / 2 - i * (lower - upper) / nbins, d)
        h.underflow().fill(-1, 3)
        h.overflow().fill(11, 1)
        return h
