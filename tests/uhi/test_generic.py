from __future__ import annotations

import numpy as np
import uhi.testing.indexing

from babyyoda import grogu
from babyyoda.histo1d import UHIHisto1D
from babyyoda.histo2d import UHIHisto2D


class TestAccess1D(uhi.testing.indexing.Indexing1D[UHIHisto1D]):
    @staticmethod
    def make_histogram() -> UHIHisto1D:
        h = grogu.Histo1D(10, 0, 10, title="test")
        data = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        for i, d in enumerate(data):
            h.fill(i + 0.5, d)
        h.underflow().fill(3)
        h.overflow().fill(1)
        return h


class TestAccess2D(uhi.testing.indexing.Indexing2D[UHIHisto2D]):
    @staticmethod
    def make_histogram() -> UHIHisto2D:
        h = grogu.Histo2D(2, 0, 2, 5, 0, 5, title="test")

        x, y = np.mgrid[0:2, 0:5]
        for i in range(2):
            for j in range(5):
                h.fill(x[i, j] + 0.5, y[i, j] + 0.5, i + j)
        return h
