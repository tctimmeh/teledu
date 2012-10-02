import unittest, os

def suite():
  testPath = os.path.split(__file__)[0]
  modules = unittest.TestLoader().discover(testPath, pattern = 'when*.py')
  return unittest.TestSuite(modules)
