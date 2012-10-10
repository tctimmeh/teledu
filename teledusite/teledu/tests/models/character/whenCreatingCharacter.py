from teledu.models import Character, CharacterAttribute, DataType, ConceptAttributeDefinition, ConceptInstance, ConceptInstanceAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreatingCharacter(TeleduTestCase):
  def setUp(self):
    super(WhenCreatingCharacter, self).setUp()
    self.name = self.uniqStr()

    self.conceptAttrDefn = self.createConceptAttrDefn()
    self.conceptInstance = ConceptInstance.objects.create(name = self.uniqStr(), concept = self.concept)
    self.conceptInstanceAttr = ConceptInstanceAttribute.objects.create(definition = self.conceptAttrDefn, instance = self.conceptInstance,
      raw_value = self.uniqStr())

    self.conceptAttrDefn = self.addAttrDefinition(type = 'concept', concept = self.concept, default = self.conceptInstance.name)

    self.character = Character.create(gameSystem = self.gameSystem, name = self.name)

  def createConceptAttrDefn(self, type = 'integer'):
    dataType = DataType.objects.get(name = type)
    return ConceptAttributeDefinition.objects.create(concept=self.concept, name=self.uniqStr(), dataType=dataType)

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

  def testThatConceptTypeAttributesGetIdOfNamedConceptInstance(self):
    actual = CharacterAttribute.objects.get(character = self.character, definition = self.conceptAttrDefn)
    self.assertEqual(int(actual.raw_value), self.conceptInstance.id)

