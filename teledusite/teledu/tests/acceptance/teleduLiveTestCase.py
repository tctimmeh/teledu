import atexit
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from teledu.tests.testHelpers import TestHelpers

driver = None
def setUpModule():
  global driver
  if driver is None:
    driver = WebDriver()

def stopDriver():
  global driver
  if driver is not None:
    driver.quit()
atexit.register(stopDriver)

class TeleduLiveTestCase(LiveServerTestCase, TestHelpers):
  urls = 'teledu.urls'

  def setUp(self):
    self.gameSystem = self.createGameSystem()
    self.character = self.createCharacter()

  @classmethod
  def setUpClass(cls):
    super(TeleduLiveTestCase, cls).setUpClass()
    global driver
    cls.driver = driver

  def url(self, path = ''):
    return '%s/%s' % (self.live_server_url, path)

