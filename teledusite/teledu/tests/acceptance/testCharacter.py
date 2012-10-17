import unittest
from selenium.common.exceptions import NoSuchElementException
from teledu.models import CharacterAttribute
from teleduLiveTestCase import TeleduLiveTestCase, setUpModule
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

  def editAttributeAndWaitForChange(self, attributeDefinition, newValue, changeDefinition = None):
    element = self.driver.find_element_by_id('attr_%d' % attributeDefinition.id)
    changeElement = element

    if changeDefinition is not None:
      changeElement = self.driver.find_element_by_id('attr_%d' % changeDefinition.id)

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
    element = self.driver.find_element_by_id('attr_%d' % self.charAttrDefn.id)
    self.assertElementTextIs(element, self.charAttr.raw_value)

  def testIntegerAttributesOnPage(self):
    element = self.driver.find_element_by_id('attr_%d' % self.intCharAttrDefn.id)
    self.assertElementTextIs(element, int(self.intCharAttr.raw_value))

  def testConceptAttributeOnPageAsConceptInstanceName(self):
    element = self.driver.find_element_by_id('attr_%d' % self.conceptCharAttrDefn.id)
    self.assertElementTextIs(element, self.conceptInstance.name)

  def testEditingTextAttributeChangesCharacterInDatabase(self):
    expected = self.uniqStr()
    self.editAttributeAndWaitForChange(self.charAttrDefn, expected)
    self.assertCharacterAttributeHasValue(self.charAttr, expected)

  def testEdittingAttributeWithDependentsUpdatesDependentAttributes(self):
    expected = self.uniqStr()
    self.editAttributeAndWaitForChange(self.charAttrDefn, expected, changeDefinition = self.dependentCharAttrDefn)
    self.assertCharacterAttributeHasValue(self.dependentCharAttr, expected)

  def testAttributeMarkedAsHiddenDoesNotAppearOnCharacterSheet(self):
    self.charAttrDefn.display = False
    self.charAttrDefn.save()
    self.driver.refresh()
    self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, 'attr_%d' % self.charAttrDefn.id)

