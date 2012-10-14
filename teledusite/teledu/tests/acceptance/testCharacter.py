from teleduLiveTestCase import TeleduLiveTestCase, setUpModule

class TestCharacterSheet(TeleduLiveTestCase):
  def setUp(self):
    super(TestCharacterSheet, self).setUp()
    self.driver.get(self.url('character/%d' % self.character.id))

  def testTitleContainsCharacterName(self):
    self.assertEqual(self.driver.title, '%s - Teledu' % self.character.name)

  def testHomeLinkGoesToWelcomePage(self):
    element = self.driver.find_element_by_partial_link_text('Home')
    element.click()
    self.assertEqual(self.driver.current_url, self.url())

  def testDeleteLinkGoesToDeleteCharacterPage(self):
    element = self.driver.find_element_by_partial_link_text('Delete')
    element.click()
    self.assertEqual(self.driver.current_url, self.url('character/%d/delete' % self.character.id))

  def testCharacterNameIsOnPage(self):
    nameElement = self.driver.find_element_by_id('attr_name')
    self.assertEqual(nameElement.text, self.character.name)

  def testTextAttributesOnPage(self):
    element = self.driver.find_element_by_id('attr_%d' % self.charAttrDefn.id)
    self.assertEqual(element.text, self.charAttr.raw_value)

  def testIntegerAttributesOnPage(self):
    element = self.driver.find_element_by_id('attr_%d' % self.intCharAttrDefn.id)
    self.assertEqual(int(element.text), int(self.intCharAttr.raw_value))

  def testConceptAttributeOnPageAsConceptInstanceName(self):
    element = self.driver.find_element_by_id('attr_%d' % self.conceptCharAttrDefn.id)
    self.assertEqual(element.text, self.conceptInstance.name)

