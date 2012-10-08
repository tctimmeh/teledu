from teledu.models import Character, CharacterAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreatingCharacter(TeleduTestCase):
  def setUp(self):
    super(WhenCreatingCharacter, self).setUp()
    self.name = self.uniqStr()
    self.character = Character.create(gameSystem = self.gameSystem, name = self.name)

  def testThatCharacterIsAddedToDatabase(self):
    self.assertTrue(self.character.id is not None)

  def testThatCharacterHaveGivenName(self):
    self.assertEqual(self.character.name, self.name)

  def testThatCharacterHasAttributesForGivenGameSystem(self):
    actual = CharacterAttribute.objects.filter(character = self.character, definition = self.attributeDefinition)
    self.assertGreater(len(actual), 0)

  def testThatAttributesGetDefaultValues(self):
    actual = CharacterAttribute.objects.get(character = self.character, definition = self.attributeDefinition)
    self.assertEqual(actual.raw_value, self.attributeDefinition.default)

