from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from teledu.tests.testHelpers import TestHelpers
from teledu.views import welcome

class TeleduLiveTestCase(LiveServerTestCase, TestHelpers):
  urls = 'teledu.urls'

  def setUp(self):
    self.gameSystem = self.createGameSystem()
    self.character = self.createCharacter()

  @classmethod
  def setUpClass(cls):
    super(TeleduLiveTestCase, cls).setUpClass()
    cls.driver = WebDriver()

  @classmethod
  def tearDownClass(cls):
    try:
      cls.driver.quit()
    except Exception, e:
      pass
    super(TeleduLiveTestCase, cls).tearDownClass()

  def url(self, path = ''):
    return '%s/%s' % (self.live_server_url, path)

