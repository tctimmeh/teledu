from teleduLiveTestCase import TeleduLiveTestCase, setUpModule

class TestWelcomePage(TeleduLiveTestCase):
  def setUp(self):
    super(TestWelcomePage, self).setUp()
    self.driver.get(self.url())

  def testPageHasWelcomeTitle(self):
    self.assertPageTitleIs('Welcome! - Teledu')

  def testCreateCharacterLinkGoesToNewCharacterPage(self):
    link = self.driver.find_element_by_partial_link_text('Create a Character')
    self.assertLinkGoesToUrl(link, 'character')

  def testAllCharactersAreLinkedOnWelcomePage(self):
    self.driver.find_element_by_link_text(self.character.name)

  def testCharacterLinksGoToCharacterPage(self):
    link = self.driver.find_element_by_link_text(self.character.name)
    self.assertLinkGoesToUrl(link, 'character/%d' % self.character.id)

