'''
Created on May 16, 2017

@author: dt186022
'''

import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../python-lib'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('python-lib-tests', pattern='*.py')
    unittest.TextTestRunner().run(all_tests)