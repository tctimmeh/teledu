from selenium.webdriver.support.select import Select
from teledu.models import Character
from teledu.tests.acceptance.teleduLiveTestCase import TeleduLiveTestCase

class TestNewCharacterPage(TeleduLiveTestCase):
  def setUp(self):
    super(TestNewCharacterPage, self).setUp()
    self.driver.get(self.url('character'))
    self.name = self.uniqStr()
    self._findFormElements()

  def _findFormElements(self):
    self.nameInput = self.driver.find_element_by_name('name')
    self.gameSystemInput = self.driver.find_element_by_name('gameSystem')
    self.gameSystemSelect = Select(self.gameSystemInput)

  def testPageHasCreateCharacterTitle(self):
    self.driver.get(self.url('character'))
    self.assertEqual(self.driver.title, 'Create Character - Teledu')

  def testSubmittingValidFormDataCreatesCharacter(self):
    self.nameInput.send_keys(self.name)
    self.gameSystemSelect.select_by_visible_text(self.gameSystem.name)
    self.nameInput.submit()

    newCharacter = Character.objects.get(name = self.name)
    self.assertEqual(self.driver.current_url, self.url('character/%d' % newCharacter.id))

  def testSubmittingWithNoNameIndicatesMissingField(self):
    self.gameSystemSelect.select_by_visible_text(self.gameSystem.name)
    self.nameInput.submit()

    self.assertEqual(self.driver.current_url, self.url('character'))
    self._findFormElements()
    errorList = self.nameInput.find_element_by_xpath("preceding-sibling::*[@class='errorlist']")
    self.assertEqual(errorList.text, "This field is required.")

  def testSubmittingWithNoNameIndicatesMissingField(self):
    self.nameInput.send_keys(self.name)
    self.nameInput.submit()

    self.assertEqual(self.driver.current_url, self.url('character'))
    self._findFormElements()
    errorList = self.gameSystemInput.find_element_by_xpath("preceding-sibling::*[@class='errorlist']")
    self.assertEqual(errorList.text, "This field is required.")

