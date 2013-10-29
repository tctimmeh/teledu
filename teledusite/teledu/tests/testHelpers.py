import random
import string
from teledu.models import GameSystem, DataType, CharacterAttribute, ConceptInstance, Character, CharacterAttributeValue, CharacterSheet, \
  Concept, CharacterAttributeDependency, ConceptAttribute, ConceptAttributeValue

class TestHelpers(object):
  def uniqInt(self):
    return random.randint(9, 999999999)

  def uniqStr(self, size = None):
    if size is None:
      size = random.randint(7,15)
    return random.choice(string.ascii_letters) + ''.join(random.choice(string.ascii_letters + string.digits) for x in range(size))

  def createGameSystem(self):
    return GameSystem.objects.create(name = self.uniqStr())

  def createAttribute(self, gameSystem = None, calcFunction = None, name = None, type = 'text', default = '',
                           concept = None, dependencies = [], list = False):
    if gameSystem is None:
      gameSystem = self.gameSystem
    if name is None:
      name = self.uniqStr()

    dataType = DataType.objects.get(name = type)

    attribute = CharacterAttribute.objects.create(pk = self.uniqInt(), gameSystem = gameSystem, name = name,
      calcFunction = calcFunction, dataType = dataType, default = default, valueConcept = concept, list = list)
    for dependency in dependencies:
      CharacterAttributeDependency.objects.create(attribute = attribute, dependency = dependency)
    return attribute

  def createCharacter(self):
    return Character.objects.create(name = self.uniqStr())

  def createAttributeValueForCharacter(self, attribute, character = None, initialValue = None):
    if character is None:
      character = self.character
    if initialValue is None:
      initialValue = attribute.default
    return CharacterAttributeValue.objects.create(character = character, attribute = attribute, raw_value = initialValue)

  def createCharacterSheetTemplate(self, gameSystem = None):
    if gameSystem is None:
      gameSystem = self.gameSystem
    return CharacterSheet.objects.create(gameSystem = gameSystem, name = self.uniqStr(), template = self.uniqStr())

  def createConcept(self, gameSystem = None, name = None):
    if gameSystem is None:
      gameSystem = self.gameSystem
    if name is None:
      name = self.uniqStr()
    return Concept.objects.create(gameSystem = gameSystem, name = name)

  def addAttributeToCharacter(self, dependencies = [], calcFunction = None, name = None, default = '', type = 'text',
                              concept = None, character = None, list = False):
    attribute = self.createAttribute(calcFunction = calcFunction, name = name, type = type, default = default,
      concept = concept, dependencies = dependencies, list = list)
    self.createAttributeValueForCharacter(attribute = attribute, character = character)
    return attribute

  def createConceptAttr(self, concept = None, name = None, type = 'text', valueConcept = None, list = False):
    if concept is None:
      concept = self.concept
    if name is None:
      name = self.uniqStr()

    dataType = DataType.objects.get(name = type)
    return ConceptAttribute.objects.create(concept=concept, name=name, dataType=dataType, valueConcept = valueConcept, list = list)

  def createConceptInstance(self, concept = None, name = None, attributes = {}):
    if concept is None:
      concept = self.concept
    if name is None:
      name = self.uniqStr()

    instance = ConceptInstance.objects.create(concept = concept, name = name)
    for attribute, value in attributes.items():
      conceptAttribute = ConceptAttributeValue.objects.get(attribute = attribute, instance = instance)
      conceptAttribute.raw_value = value
      conceptAttribute.save()
    return instance

  def assertCharacterAttributeHasRawValue(self, attribute, expected):
    if isinstance(attribute, CharacterAttributeValue):
      actual = CharacterAttributeValue.objects.get(attribute = attribute.attribute, character = self.character).raw_value
    else:
      actual = CharacterAttributeValue.objects.get(attribute = attribute, character = self.character).raw_value
    self.assertEqual(actual, unicode(expected))

  def getCharacterAttributeValueObject(self, attribute, character = None):
    if character is None:
      character = self.character

    return CharacterAttributeValue.objects.get(attribute = attribute, character = character)

  def getCharacterAttributeValue(self, attribute, character = None):
    if character is None:
      character = self.character
    return attribute.getValue(character)

  def getCharacterAttributeRawValue(self, attribute, character = None):
    attribute = self.getCharacterAttributeValueObject(attribute, character)
    return attribute.raw_value

  def assertCharacterHasAttributeValue(self, attribute):
    CharacterAttributeValue.objects.get(character = self.character, attribute = attribute)

