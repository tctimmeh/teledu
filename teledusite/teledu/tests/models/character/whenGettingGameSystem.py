from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingCharacterGameSystem(TeleduTestCase):
  def testThatCorrectGameSystemIsReturned(self):
    actual = self.character.gameSystem
    self.assertEqual(actual, self.gameSystem)


