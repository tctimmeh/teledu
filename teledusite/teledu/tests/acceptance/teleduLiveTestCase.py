import atexit
import random
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
    self.concept = self.createConcept()
    self.conceptInstance = self.createConceptInstance()
    self.character = self.createCharacter()
    self.charAttrDefn = self.createAttrDefinition(default = self.uniqStr())
    self.charAttr = self.createAttrForCharacter(self.charAttrDefn)
    self.intCharAttrDefn = self.createAttrDefinition(type = 'integer', default = self.uniqInt())
    self.intCharAttr = self.createAttrForCharacter(self.intCharAttrDefn)
    self.conceptCharAttrDefn = self.createAttrDefinition(type = 'concept', concept = self.concept)
    self.conceptCharAttr = self.createAttrForCharacter(self.conceptCharAttrDefn, initialValue = self.conceptInstance.id)

  @classmethod
  def setUpClass(cls):
    super(TeleduLiveTestCase, cls).setUpClass()
    global driver
    cls.driver = driver

  def url(self, path = ''):
    return '%s/%s' % (self.live_server_url, path)

