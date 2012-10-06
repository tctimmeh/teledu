from teledu.tests.teleduTestCase import TeleduTestCase

class WhenViewingCharacterSheetAsJson(TeleduTestCase):
  def setUp(self):
    super(WhenViewingCharacterSheetAsJson, self).setUp()
    self.response = self.client.get('/character/%d.json' % self.character.id)

  def testThatResponseTextIsCharacterAsJson(self):
    self.assertEqual(self.response.content, self.character.serialize())
