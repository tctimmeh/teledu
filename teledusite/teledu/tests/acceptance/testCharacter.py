from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from teledu.models import CharacterAttributeValue
from teleduLiveTestCase import TeleduLiveTestCase
from selenium.webdriver.support.ui import WebDriverWait

class TestCharacterSheet(TeleduLiveTestCase):
  def setUp(self):
    super(TestCharacterSheet, self).setUp()
    self.driver.get(self.url('character/%d' % self.character.id))

  def editElement(self, element, newValue):
    element.click()
    input = element.find_element_by_tag_name('input')
    input.clear()
    input.send_keys(newValue)
    input.submit()

  def editAttributeAndWaitForChange(self, attribute, newValue, changeAttribute = None):
    element = self.driver.find_element_by_id('attr_%d' % attribute.id)
    changeElement = element

    if changeAttribute is not None:
      changeElement = self.driver.find_element_by_id('attr_%d' % changeAttribute.id)

    self.editElement(element, newValue)
    WebDriverWait(self.driver, 5).until(lambda driver: self.elementHasText(changeElement, newValue))

  def testTitleContainsCharacterName(self):
    self.assertPageTitleIs('%s - Teledu' % self.character.name)

  def testHomeLinkGoesToWelcomePage(self):
    element = self.driver.find_element_by_partial_link_text('Home')
    self.assertLinkGoesHome(element)

  def testDeleteLinkGoesToDeleteCharacterPage(self):
    element = self.driver.find_element_by_partial_link_text('Delete')
    self.assertLinkGoesToUrl(element, 'character/%d/delete' % self.character.id)

  def testCharacterNameIsOnPage(self):
    nameElement = self.driver.find_element_by_id('attr_name')
    self.assertElementTextIs(nameElement, self.character.name)

  def testTextAttributesOnPage(self):
    element = self.driver.find_element_by_id('attr_%d' % self.charAttr.id)
    self.assertElementTextIs(element, self.charAttrValue.raw_value)

  def testIntegerAttributesOnPage(self):
    element = self.driver.find_element_by_id('attr_%d' % self.intCharAttr.id)
    self.assertElementTextIs(element, int(self.intCharAttrValue.raw_value))

  def testConceptAttributeOnPageAsConceptInstanceName(self):
    element = self.driver.find_element_by_id('attr_%d' % self.conceptCharAttr.id)
    self.assertElementTextIs(element, self.conceptInstance.name)

  def testEditingTextAttributeChangesCharacterInDatabase(self):
    expected = self.uniqStr()
    self.editAttributeAndWaitForChange(self.charAttr, expected)
    self.assertCharacterAttributeHasRawValue(self.charAttrValue, expected)

  def testEditingAttributeWithDependentsUpdatesDependentAttributes(self):
    expected = self.uniqStr()
    self.editAttributeAndWaitForChange(self.charAttr, expected, changeAttribute = self.dependentCharAttr)
    self.assertCharacterAttributeHasRawValue(self.dependentCharAttr, expected)

  def testAttributeMarkedAsHiddenDoesNotAppearOnCharacterSheet(self):
    self.charAttr.display = False
    self.charAttr.save()
    self.driver.refresh()
    self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, 'attr_%d' % self.charAttr.id)

  def testChoosingNewValueForConceptAttributeUpdatesCharacterInDatabase(self):
    conceptInstance2 = self.createConceptInstance()

    element = self.driver.find_element_by_id('attr_%d' % self.conceptCharAttr.id)
    element.click()
    select = Select(element.find_element_by_tag_name('select'))
    self.assertEqual(select.first_selected_option.text, self.conceptInstance.name)

    select.select_by_visible_text(conceptInstance2.name)
    WebDriverWait(self.driver, 5).until(lambda driver: self.elementHasText(element, conceptInstance2.name))

    expected = conceptInstance2.name
    actual = CharacterAttributeValue.objects.get(character = self.character, attribute = self.conceptCharAttr).value
    self.assertEqual(actual, expected)

  def testListAttributesDisplayedAsUnorderedList(self):
    self.charAttr.list = True
    self.charAttr.save()
    attr2 = self.createAttributeValueForCharacter(self.charAttr, initialValue = self.uniqStr())
    self.driver.refresh()

    expected = [self.charAttrValue.value, attr2.value]
    expected.sort()

    element = self.driver.find_element_by_id('attr_%d' % self.charAttr.id)
    self.assertTrue(element.tag_name, 'ul')

    items = element.find_elements_by_tag_name('li')
    actual = map(lambda e: e.text, items)
    actual.sort()

    self.assertEqual(actual, expected)

