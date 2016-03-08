#!/usr/bin/env python3
"""Main test runner for auacm"""

import unittest, sys

if __name__ == '__main__':
    unittest.TextTestRunner().run(
        unittest.defaultTestLoader.discover(
            start_dir='.',
            pattern='*_tests.py'))
