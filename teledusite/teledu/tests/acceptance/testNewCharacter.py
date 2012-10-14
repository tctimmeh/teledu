from selenium.webdriver.support.select import Select
from teledu.models import Character
from teleduLiveTestCase import TeleduLiveTestCase, setUpModule

class TestNewCharacterPage(TeleduLiveTestCase):
  def setUp(self):
    super(TestNewCharacterPage, self).setUp()
    self.pageUrl = 'character'

    self.driver.get(self.url(self.pageUrl))
    self.name = self.uniqStr()
    self._findFormElements()

  def _findFormElements(self):
    self.nameInput = self.driver.find_element_by_name('name')
    self.gameSystemInput = self.driver.find_element_by_name('gameSystem')
    self.gameSystemSelect = Select(self.gameSystemInput)

  def assertReturnedToForm(self):
    self.assertLocationIs(self.pageUrl)
    self._findFormElements()

  def testPageHasCreateCharacterTitle(self):
    self.assertPageTitleIs('Create Character - Teledu')

  def testSubmittingValidFormDataCreatesCharacter(self):
    self.nameInput.send_keys(self.name)
    self.gameSystemSelect.select_by_visible_text(self.gameSystem.name)

    self.submitForm()
    newCharacter = Character.objects.get(name = self.name)
    self.assertLocationIs('character/%d' % newCharacter.id)

  def testSubmittingWithNoNameIndicatesMissingField(self):
    self.gameSystemSelect.select_by_visible_text(self.gameSystem.name)

    self.nameInput.submit()
    self.assertReturnedToForm()
    self.assertFormFieldHasRequiredError(self.nameInput)

  def testSubmittingWithNoNameIndicatesMissingField(self):
    self.nameInput.send_keys(self.name)

    self.nameInput.submit()
    self.assertReturnedToForm()
    self.assertFormFieldHasRequiredError(self.gameSystemInput)

