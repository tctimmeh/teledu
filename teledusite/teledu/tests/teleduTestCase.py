from django.test import TestCase
from teledu.models import GameSystem, CharacterAttributeDefinition, Character, CharacterAttribute

class TeleduTestCase(TestCase):
  def setUp(self):
    self.gameSystem = GameSystem.objects.create(name = 'something')
    self.attributeDefinition = CharacterAttributeDefinition.objects.create(gameSystem = self.gameSystem, name = 'whatever')
    self.character = Character.objects.create(name = 'whomever')
    self.attributeValue = 'a testing value'
    self.charAttr = CharacterAttribute.objects.create(character = self.character, definition = self.attributeDefinition, value = self.attributeValue)

