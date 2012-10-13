from teledu.tests.acceptance.teleduLiveTestCase import TeleduLiveTestCase

class WhenTryingSelenium(TeleduLiveTestCase):
  def testWelcomePage(self):
    self.driver.get(self.url())
    self.assertEqual(self.driver.title, 'Welcome! - Teledu')

  def testCreateCharacter(self):
    self.driver.get(self.url())
    link = self.driver.find_element_by_partial_link_text('Create a Character')
    link.click()
    self.assertEqual(self.driver.current_url, self.url('character'))

