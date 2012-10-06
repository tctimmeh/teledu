import random, string
from django.test import TestCase
from teledu.models import GameSystem, CharacterAttributeDefinition, Character, CharacterAttribute, CharacterSheet

random.seed(0x5ADB0075)

class TeleduTestCase(TestCase):
  urls = 'teledu.urls'

  def setUp(self):
    self.gameSystem = self.createGameSystem()
    self.attributeDefinition = self.createAttrDefinition(self.gameSystem)
    self.character = self.createCharacter()
    self.attributeValue = self.uniqStr()
    self.charAttr = self.createAttrForCharacter(self.attributeDefinition, self.character, self.attributeValue)
    self.charSheetTemplate = self.createCharacterSheetTemplate()

  def uniqStr(self, size = None):
    if size is None:
      size = random.randint(7,15)
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(size))

  def createGameSystem(self):
    return GameSystem.objects.create(name = self.uniqStr())

  def createAttrDefinition(self, gameSystem = None, calcFunction = None):
    if gameSystem is None:
      gameSystem = self.gameSystem
    return CharacterAttributeDefinition.objects.create(gameSystem = gameSystem, name = self.uniqStr(), calcFunction = calcFunction)

  def createCharacter(self):
    return Character.objects.create(name = self.uniqStr())

  def createAttrForCharacter(self, attrDefinition, character = None, initialValue = None):
    if character is None:
      character = self.character
    if initialValue is None:
      initialValue = self.uniqStr()
    return CharacterAttribute.objects.create(character = character, definition = attrDefinition, value = initialValue)

  def createCharacterSheetTemplate(self, gameSystem = None):
    if gameSystem is None:
      gameSystem = self.gameSystem
    return CharacterSheet.objects.create(gameSystem = gameSystem, name = self.uniqStr(), template = self.uniqStr())
    
