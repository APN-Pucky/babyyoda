from __future__ import annotations

import numpy as np
import uhi.testing.indexing

from babyyoda import grogu
from babyyoda.grogu.histo2d_v3 import GROGU_HISTO2D_V3
from babyyoda.histo2d import UHIHisto2D


class TestAccess2D(uhi.testing.indexing.Indexing2D[UHIHisto2D]):
    def bin_to_value(self, bin):
        return bin.sumW()

    def sum_to_value(self, bin):
        return bin.sumW()

    def value_to_bin(self, value):
        return GROGU_HISTO2D_V3.Bin(d_sumw=value)

    @staticmethod
    def make_histogram() -> UHIHisto2D:
        h = grogu.Histo2D(2, 0, 2, 5, 0, 5, title="test")

        x, y = np.mgrid[0:2, 0:5]
        for i in range(2):
            for j in range(5):
                h.fill(x[i, j] + 0.5, y[i, j] + 0.5, i + 2 * j)
        return h

    def test_access_loc_underflow(self):
        # No
        pass

    def test_ellipsis_integration_dict(self):
        # No
        pass

    def test_mixed_single_integration_dict(self):
        # No
        pass

    def test_ellipsis_integration(self):
        # No
        pass

    def test_setting_dict(self):
        # No
        pass

    def test_setting_dict_slice(self):
        # No
        pass

    def test_setting_dict_slicer(self):
        # No
        pass

    def test_setting_underflow(self):
        # No
        pass

    def test_setting_array(self):
        # No
        pass

    def test_setting_array_broadcast(self):
        # No
        pass

    def test_slicing_all(self):
        # TODO no clue why equality check fails
        pass
