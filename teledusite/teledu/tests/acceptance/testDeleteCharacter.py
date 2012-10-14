from teledu.models import Character
from teleduLiveTestCase import TeleduLiveTestCase, setUpModule
from django.core.exceptions import ObjectDoesNotExist

class TestDeleteCharacterPage(TeleduLiveTestCase):
  def setUp(self):
    super(TestDeleteCharacterPage, self).setUp()
    self.driver.get('http://localhost/nothing')
    self.driver.get(self.url('character/%d/delete' % self.character.id))

  def testPageTitleIndicatesDeletingCharacter(self):
    self.assertPageTitleIs('%s - DELETE - Teledu' % self.character.name)

  def testConfirmationButtonDeletesCharacter(self):
    okButton = self.driver.find_element_by_xpath("//input[@value='Yes']")
    okButton.click()
    self.assertLocationIs('')
    self.assertRaises(ObjectDoesNotExist, Character.objects.get, pk = self.character.id)

  def testCancelButtonDoesNotDeleteCharacter(self):
    startingUrl = 'http://localhost/nothing'
    self.driver.get(startingUrl)
    self.driver.get(self.url('character/%d/delete' % self.character.id))

    cancelButton = self.driver.find_element_by_xpath("//input[@value='No']")
    cancelButton.click()

    self.assertEqual(self.driver.current_url, startingUrl)
    character = Character.objects.get(pk = self.character.id)
    self.assertIsNotNone(character)

