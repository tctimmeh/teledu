from teledu.models import Character, ConceptInstance, CharacterAttributeValue
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreatingCharacter(TeleduTestCase):
  def setUp(self):
    super(WhenCreatingCharacter, self).setUp()
    self.name = self.uniqStr()

    self.conceptInstance = ConceptInstance.objects.create(name = self.uniqStr(), concept = self.concept)

    self.conceptAttrDefn = self.addAttrDefnToCharacter(type = 'concept', concept = self.concept, default = self.conceptInstance.name)
    self.noDefaultDefn = self.createAttrDefinition(type = 'concept', concept = self.concept)
    self.character = Character.create(gameSystem = self.gameSystem, name = self.name)

  def testThatCharacterHasAttributesForGivenGameSystem(self):
    actual = CharacterAttributeValue.objects.filter(character = self.character, definition = self.charAttrDefn)
    self.assertGreater(len(actual), 0)

  def testThatAttributesGetDefaultValues(self):
    actual = self.getCharacterAttributeRawValueByDefinition(self.charAttrDefn)
    self.assertEqual(actual, self.charAttrDefn.default)

  def testThatConceptTypeAttributesGetIdOfNamedConceptInstance(self):
    actual = self.getCharacterAttributeRawValueByDefinition(self.conceptAttrDefn)
    self.assertEqual(int(actual), self.conceptInstance.id)

  def testThatConceptTypeAttributesGetEmptyValueForDefinitionsWithNoDefault(self):
    actual = self.getCharacterAttributeRawValueByDefinition(self.noDefaultDefn)
    self.assertEqual(actual, '')

