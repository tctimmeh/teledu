from django.core.exceptions import ObjectDoesNotExist
from teledu.models import CharacterAttribute, CharacterAttributeDefinition, ConceptInstance
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenAddingMissingAttributes(TeleduTestCase):
  def testAllMissingAttributesAreAdded(self):
    self.createAttrDefinition(name="newDefinition")
    self.character.addMissingCharacterAttributeDefinitions()
    characterAttributeDefinitions = CharacterAttributeDefinition.objects.filter(gameSystem = self.gameSystem)
    for attributeDefinition in characterAttributeDefinitions:
      CharacterAttribute.objects.get(character = self.character, definition = attributeDefinition)

  def testCorrectDefaultValueIsAssignedIfNotConcept(self):
    newAttributeDefinition = self.createAttrDefinition(name="newDefinition")
    self.character.addMissingCharacterAttributeDefinitions()
    expectedValue = newAttributeDefinition.default
    attribute = CharacterAttribute.objects.get(character = self.character, definition = newAttributeDefinition)
    self.assertEqual(expectedValue, attribute.raw_value)

  def testCorrectDefaultValueIsAssignedIfConcept(self):
    newAttributeDefinition = self.createAttrDefinition(name="newDefinition", concept=self.concept)
    self.character.addMissingCharacterAttributeDefinitions()
    try:
      expectedValue = ConceptInstance.objects.get(name = self.concept.name, concept = self.concept).id
    except ObjectDoesNotExist, e:
      expectedValue = ''
    attribute = CharacterAttribute.objects.get(character = self.character, definition = newAttributeDefinition)
    self.assertEqual(expectedValue, attribute.raw_value)




