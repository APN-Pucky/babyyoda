from __future__ import annotations

import uhi.testing.indexing

from babyyoda import grogu
from babyyoda.histo1d import UHIHisto1D


class TestAccess(uhi.testing.indexing.Indexing1D[UHIHisto1D]):
    @staticmethod
    def make_histogram() -> UHIHisto1D:
        h = grogu.Histo1D(10, 0, 10, title="test")
        data = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        for i, d in enumerate(data):
            h.fill(i + 0.5, d)
        h.underflow().fill(3)
        h.overflow().fill(1)
        return h
