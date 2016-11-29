import unittest

import numpy as np
import Orange
from orangecontrib.infrared.data import getx
from orangecontrib.infrared.preprocess import features_with_interpolation


class TestReaders(unittest.TestCase):

    def test_peach_juice(self):
        d1 = Orange.data.Table("peach_juice.dpt")
        d2 = Orange.data.Table("peach_juice.0")
        #dpt file has rounded values
        np.testing.assert_allclose(d1.X, d2.X, atol=1e-5)

    def test_autointerpolate(self):
        d1 = Orange.data.Table("peach_juice.dpt")
        d2 = Orange.data.Table("collagen.csv")
        d3 = Orange.data.Table(d1.domain, d2)
        d1x = getx(d1)
        d2x = getx(d2)

        #have the correct number of non-nan elements
        validx = np.where(d1x >= min(d2x), d1x, np.nan)
        validx = np.where(d1x <= max(d2x), validx, np.nan)
        self.assertEqual(np.sum(~np.isnan(validx)),
                         np.sum(~np.isnan(d3.X[0])))

        #check roundtrip
        atts = features_with_interpolation(d2x)
        ndom = Orange.data.Domain(atts, None)
        dround = Orange.data.Table(ndom, d3)
        #edges are unknown, the rest roughly the same
        np.testing.assert_allclose(dround.X[:, 1:-1], d2.X[:, 1:-1], rtol=0.011)


class TestGSS(unittest.TestCase):

    def test_open(self):
        data = Orange.data.Table("Au168mA_nodisplacement.gsf")
        self.assertEquals(data.X.shape, (1, 20480))


class TestNea(unittest.TestCase):

    def test_open(self):
        data = Orange.data.Table("/home/marko/spectra20.nea")
        self.assertEqual(len(data), 12)
        # FIXME check contents