from teledu.models import Character, ConceptInstance, CharacterAttributeValue
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreatingCharacter(TeleduTestCase):
  def setUp(self):
    super(WhenCreatingCharacter, self).setUp()
    self.name = self.uniqStr()

    self.conceptInstance = ConceptInstance.objects.create(name = self.uniqStr(), concept = self.concept)

    self.conceptAttr = self.addAttributeToCharacter(type = 'concept', concept = self.concept, default = self.conceptInstance.name)
    self.noDefaultAttribute = self.createAttribute(type = 'concept', concept = self.concept)
    self.character = Character.create(gameSystem = self.gameSystem, name = self.name)

  def testThatCharacterHasAttributesForGivenGameSystem(self):
    actual = CharacterAttributeValue.objects.filter(character = self.character, attribute = self.charAttr)
    self.assertGreater(len(actual), 0)

  def testThatAttributesGetDefaultValues(self):
    actual = self.getCharacterAttributeRawValue(self.charAttr)
    self.assertEqual(actual, self.charAttr.default)

  def testThatConceptTypeAttributesGetIdOfNamedConceptInstance(self):
    actual = self.getCharacterAttributeRawValue(self.conceptAttr)
    self.assertEqual(int(actual), self.conceptInstance.id)

  def testThatConceptTypeAttributesGetEmptyValueWhenNoDefaultIsGiven(self):
    actual = self.getCharacterAttributeRawValue(self.noDefaultAttribute)
    self.assertEqual(actual, '')

