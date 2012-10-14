from teleduLiveTestCase import TeleduLiveTestCase, setUpModule

class TestWelcomePage(TeleduLiveTestCase):
  def testPageHasWelcomeTitle(self):
    self.driver.get(self.url())
    self.assertEqual(self.driver.title, 'Welcome! - Teledu')

  def testCreateCharacterLinkGoesToNewCharacterPage(self):
    self.driver.get(self.url())
    link = self.driver.find_element_by_partial_link_text('Create a Character')
    link.click()
    self.assertEqual(self.driver.current_url, self.url('character'))

  def testAllCharactersAreLinkedOnWelcomePage(self):
    self.driver.get(self.url())
    self.driver.find_element_by_link_text(self.character.name)

  def testCharacterLinksGoToCharacterPage(self):
    self.driver.get(self.url())
    link = self.driver.find_element_by_link_text(self.character.name)
    link.click()
    self.assertEqual(self.driver.current_url, self.url('character/%d' % self.character.id))

