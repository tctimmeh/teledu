import unittest, os
from django.db.models import get_app
from django.test.simple import DjangoTestSuiteRunner, build_test, build_suite
from django.utils.unittest.suite import TestSuite

class TeleduTestRunner(DjangoTestSuiteRunner):
  testPath = os.path.split(__file__)[0]

  def _loadTestsFromLabel(self, label):
    testPath = os.path.join(self.testPath, label)
    return unittest.TestLoader().discover(start_dir = testPath)

  def build_suite(self, test_labels, extra_tests=None, **kwargs):
    if not test_labels:
      return super(TeleduTestRunner, self).build_suite(test_labels, extra_tests, **kwargs)

    suite = TestSuite()

    for label in test_labels:
      parts = label.split('.')
      if parts[0].lower() == 'teledu':
        if len(parts) < 2:
          suite.addTest(unittest.TestLoader().discover(start_dir = self.testPath, pattern = 'when*.py'))
        else:
          suite.addTest(self._loadTestsFromLabel(parts[1]))
      else:
        if '.' in label:
          suite.addTest(build_test(label))
        else:
          app = get_app(label)
          suite.addTest(build_suite(app))

    if extra_tests:
      for test in extra_tests:
        suite.addTest(test)

    return suite

