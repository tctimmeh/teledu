import random
import string
from teledu.models import GameSystem, DataType, CharacterAttributeDefinition, Character, CharacterAttribute, CharacterSheet, GameSystemConcept, CharacterAttributeDependency, ConceptAttributeDefinition, ConceptInstance

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
                           concept = None, dependencies = []):
    if gameSystem is None:
      gameSystem = self.gameSystem
    if name is None:
      name = self.uniqStr()

    dataType = DataType.objects.get(name = type)

    definition = CharacterAttributeDefinition.objects.create(pk = self.uniqInt(), gameSystem = gameSystem, name = name,
      calcFunction = calcFunction, dataType = dataType, default = default, concept = concept)
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
    return CharacterAttribute.objects.create(character = character, definition = attrDefinition, raw_value = initialValue)

  def createCharacterSheetTemplate(self, gameSystem = None):
    if gameSystem is None:
      gameSystem = self.gameSystem
    return CharacterSheet.objects.create(gameSystem = gameSystem, name = self.uniqStr(), template = self.uniqStr())

  def createConcept(self, gameSystem = None, name = None):
    if gameSystem is None:
      gameSystem = self.gameSystem
    if name is None:
      name = self.uniqStr()
    return GameSystemConcept.objects.create(gameSystem = gameSystem, name = name)

  def addAttrDefinition(self, dependencies = [], calcFunction = None, name = None, default = '', type = 'text', concept = None):
    definition = self.createAttrDefinition(calcFunction = calcFunction, name = name, type = type, default = default,
      concept = concept, dependencies = dependencies)
    self.createAttrForCharacter(attrDefinition = definition)
    return definition

  def createConceptAttrDefn(self, concept = None, name = None, type = 'integer'):
    if concept is None:
      concept = self.concept
    if name is None:
      name = self.uniqStr()

    dataType = DataType.objects.get(name = type)
    return ConceptAttributeDefinition.objects.create(concept=concept, name=name, dataType=dataType)

  def createConceptInstance(self, concept = None, name = None):
    if concept is None:
      concept = self.concept
    if name is None:
      name = self.uniqStr()

    return ConceptInstance.objects.create(concept = concept, name = name)

  def assertCharacterAttributeHasValue(self, attr, expected):
    actual = CharacterAttribute.objects.get(pk = attr.id).raw_value
    self.assertEqual(actual, expected)

