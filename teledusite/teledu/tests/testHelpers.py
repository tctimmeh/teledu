import random
import string
from teledu.models import GameSystem, DataType, CharacterAttribute, Character, CharacterAttributeValue, CharacterSheet, \
  Concept, CharacterAttributeDependency, ConceptAttribute, ConceptInstance, ConceptAttributeValue

class TestHelpers(object):
  def uniqInt(self):
    return random.randint(9, 999999999)

  def uniqStr(self, size = None):
    if size is None:
      size = random.randint(7,15)
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(size))

  def createGameSystem(self):
    return GameSystem.objects.create(name = self.uniqStr())

  def createAttrDefinition(self, gameSystem = None, calcFunction = None, name = None, type = 'text', default = '',
                           concept = None, dependencies = [], list = False):
    if gameSystem is None:
      gameSystem = self.gameSystem
    if name is None:
      name = self.uniqStr()

    dataType = DataType.objects.get(name = type)

    definition = CharacterAttribute.objects.create(pk = self.uniqInt(), gameSystem = gameSystem, name = name,
      calcFunction = calcFunction, dataType = dataType, default = default, valueConcept = concept, list = list)
    for dependency in dependencies:
      CharacterAttributeDependency.objects.create(attribute = definition, dependency = dependency)
    return definition

  def createCharacter(self):
    return Character.objects.create(name = self.uniqStr())

  def createAttrForCharacter(self, attrDefinition, character = None, initialValue = None):
    if character is None:
      character = self.character
    if initialValue is None:
      initialValue = attrDefinition.default
    return CharacterAttributeValue.objects.create(character = character, definition = attrDefinition, raw_value = initialValue)

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

  def addAttrDefnToCharacter(self, dependencies = [], calcFunction = None, name = None, default = '', type = 'text', concept = None, character = None):
    definition = self.createAttrDefinition(calcFunction = calcFunction, name = name, type = type, default = default,
      concept = concept, dependencies = dependencies)
    self.createAttrForCharacter(attrDefinition = definition, character = character)
    return definition

  def createConceptAttrDefn(self, concept = None, name = None, type = 'integer'):
    if concept is None:
      concept = self.concept
    if name is None:
      name = self.uniqStr()

    dataType = DataType.objects.get(name = type)
    return ConceptAttribute.objects.create(concept=concept, name=name, dataType=dataType)

  def createConceptInstance(self, concept = None, name = None, attributes = {}):
    if concept is None:
      concept = self.concept
    if name is None:
      name = self.uniqStr()

    instance = ConceptInstance.objects.create(concept = concept, name = name)
    for definition, value in attributes.items():
      conceptAttribute = ConceptAttributeValue.objects.get(definition = definition, instance = instance)
      conceptAttribute.raw_value = value
      conceptAttribute.save()
    return instance

  def assertCharacterAttributeHasRawValue(self, attr, expected):
    if isinstance(attr, CharacterAttributeValue):
      actual = CharacterAttributeValue.objects.get(pk = attr.id).raw_value
    else:
      actual = CharacterAttributeValue.objects.get(definition = attr, character = self.character).raw_value
    self.assertEqual(actual, unicode(expected))

  def getCharacterAttributeForDefinition(self, definition, character = None):
    if character is None:
      character = self.character

    return CharacterAttributeValue.objects.get(definition = definition, character = character)

  def getCharacterAttributeValueByDefinition(self, definition, character = None):
    attribute = self.getCharacterAttributeForDefinition(definition, character)
    return attribute.value

  def getCharacterAttributeRawValueByDefinition(self, definition, character = None):
    attribute = self.getCharacterAttributeForDefinition(definition, character)
    return attribute.raw_value

  def assertCharacterHasAttributeForDefinition(self, definition):
    CharacterAttributeValue.objects.get(character = self.character, definition = definition)

