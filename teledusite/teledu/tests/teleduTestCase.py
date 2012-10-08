import random, string
from django.test import TestCase
from teledu.models import GameSystem, CharacterAttributeDefinition, Character, CharacterAttribute, CharacterSheet, CharacterAttributeDependency
from teledu.models.dataType import DataType

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

  def uniqInt(self):
    return random.randint(9, 999999999)

  def uniqStr(self, size = None):
    if size is None:
      size = random.randint(7,15)
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(size))

  def createGameSystem(self):
    return GameSystem.objects.create(name = self.uniqStr())

  def createAttrDefinition(self, gameSystem = None, calcFunction = None, name = None, type = 'text', default = ''):
    if gameSystem is None:
      gameSystem = self.gameSystem
    if name is None:
      name = self.uniqStr()

    dataType = DataType.objects.get(name = type)

    return CharacterAttributeDefinition.objects.create(pk = self.uniqInt(), gameSystem = gameSystem, name = name,
      calcFunction = calcFunction, dataType = dataType, default = default)

  def createCharacter(self):
    return Character.objects.create(name = self.uniqStr())

  def createAttrForCharacter(self, attrDefinition, character = None, initialValue = None):
    if character is None:
      character = self.character
    if initialValue is None:
      initialValue = attrDefinition.default
    return CharacterAttribute.objects.create(character = character, definition = attrDefinition, raw_value = initialValue)

  def createCharacterSheetTemplate(self, gameSystem = None):
    if gameSystem is None:
      gameSystem = self.gameSystem
    return CharacterSheet.objects.create(gameSystem = gameSystem, name = self.uniqStr(), template = self.uniqStr())

  def addAttrDefinition(self, dependencies = [], calcFunction = None, name = None, default = '', type = 'text'):
    attr = self.createAttrDefinition(calcFunction = calcFunction, name = name, type = type, default = default)
    self.createAttrForCharacter(attrDefinition = attr)
    for dependency in dependencies:
      CharacterAttributeDependency.objects.create(attribute = attr, dependency = dependency)
    return attr


