# -*- coding: utf-8 -*-

import doctest
from os.path import join

from pkg_resources import resource_listdir

import unittest2 as unittest
from senaite.storage.config import PRODUCT_NAME
from senaite.storage.tests.base import SimpleTestCase
from Testing import ZopeTestCase as ztc

rst_filenames = [f for f in resource_listdir(PRODUCT_NAME, "tests/doctests")
                 if f.endswith(".rst")]

doctests = [join("doctests", filename) for filename in rst_filenames]

flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF


def test_suite():
    suite = unittest.TestSuite()
    for doctestfile in doctests:
        suite.addTests([
            ztc.ZopeDocFileSuite(
                doctestfile,
                test_class=SimpleTestCase,
                optionflags=flags
            )
        ])
    return suite
