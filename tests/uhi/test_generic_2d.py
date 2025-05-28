from __future__ import annotations

import numpy as np
import uhi.testing.indexing

from babyyoda import grogu
from babyyoda.histo2d import UHIHisto2D


class TestAccess2D(uhi.testing.indexing.Indexing2D[UHIHisto2D]):
    def get_value(self, bin):
        return bin.sumW()

    @staticmethod
    def make_histogram() -> UHIHisto2D:
        h = grogu.Histo2D(2, 0, 2, 5, 0, 5, title="test")

        x, y = np.mgrid[0:2, 0:5]
        for i in range(2):
            for j in range(5):
                h.fill(x[i, j] + 0.5, y[i, j] + 0.5, i + j)
        return h
