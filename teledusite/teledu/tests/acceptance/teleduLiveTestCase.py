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
    self.concept = self.createConcept()
    self.conceptInstance = self.createConceptInstance()
    self.character = self.createCharacter()

    self.charAttr = self.createAttribute(default = self.uniqStr())
    self.charAttrValue = self.createAttributeValueForCharacter(self.charAttr)

    self.intCharAttr = self.createAttribute(type = 'integer', default = self.uniqInt())
    self.intCharAttrValue = self.createAttributeValueForCharacter(self.intCharAttr)

    self.conceptCharAttr = self.createAttribute(type = 'concept', concept = self.concept)
    self.conceptCharAttrValue = self.createAttributeValueForCharacter(self.conceptCharAttr, initialValue = self.conceptInstance.id)

    self.dependentCharAttr = self.createAttribute(calcFunction = "result = attr('%s')" % self.charAttr.name,
      dependencies = [self.charAttr])
    self.dependentCharAttrValue = self.createAttributeValueForCharacter(self.dependentCharAttr)

  @classmethod
  def setUpClass(cls):
    super(TeleduLiveTestCase, cls).setUpClass()
    global driver
    cls.driver = driver

  def url(self, path = ''):
    return '%s/%s' % (self.live_server_url, path)

  def elementHasText(self, element, expected):
    return element.text == expected

  def assertElementTextIs(self, element, expected):
    self.assertEqual(element.text, unicode(expected))

  def assertLinkGoesHome(self, link):
    self.assertLinkGoesToUrl(link, '')

  def assertLinkGoesToUrl(self, link, expectedUrl):
    link.click()
    self.assertLocationIs(expectedUrl)

  def assertPageTitleIs(self, expected):
    self.assertEqual(self.driver.title, expected)

  def assertLocationIs(self, expected):
    self.assertEqual(self.driver.current_url, self.url(expected))

  def assertFormFieldHasRequiredError(self, element):
    errorList = element.find_element_by_xpath("preceding-sibling::*[@class='errorlist']")
    self.assertEqual(errorList.text, "This field is required.")

  def submitForm(self):
    submitButton = self.driver.find_element_by_xpath("//input[@type='submit']")
    submitButton.click()

