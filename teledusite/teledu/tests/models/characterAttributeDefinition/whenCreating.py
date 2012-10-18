from teledu.models import CharacterAttributeDefinition
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreatingCharacterAttributeDefinition(TeleduTestCase):
  def testDefaultDisplayValueIsTrue(self):
    characterAttributeDefinition = CharacterAttributeDefinition.objects.create(gameSystem = self.gameSystem, name = self.uniqStr())
    self.assertTrue(characterAttributeDefinition.display)
