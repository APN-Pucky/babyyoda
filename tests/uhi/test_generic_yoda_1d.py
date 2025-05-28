from __future__ import annotations

import uhi.testing.indexing

from babyyoda.histo1d import UHIHisto1D
from babyyoda.test import init_yoda

yoda, yoda_available, yoda2 = init_yoda()


class TestAccess1D(uhi.testing.indexing.Indexing1D[UHIHisto1D]):
    def get_value(self, bin):
        return bin.sumW()

    @staticmethod
    def make_histogram() -> UHIHisto1D:
        nbins = 10
        lower = 0
        upper = 1
        h = yoda.Histo1D(10, 0, 1, title="test")
        data = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        for i, d in enumerate(data):
            h.fill(lower - (lower - upper) / nbins / 2 - i * (lower - upper) / nbins, d)
        h.underflow().fill(-1, 3)
        h.overflow().fill(11, 1)
        return h
