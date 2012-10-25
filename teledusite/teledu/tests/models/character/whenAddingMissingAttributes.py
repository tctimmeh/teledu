from django.core.exceptions import ObjectDoesNotExist
from teledu.models import CharacterAttribute, ConceptInstance
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenAddingMissingAttributes(TeleduTestCase):
  def testAllMissingAttributesAreAdded(self):
    definition = self.createAttrDefinition()
    definition2 = self.createAttrDefinition()
    self.character.addMissingCharacterAttributeDefinitions()
    self.assertCharacterHasAttributeForDefinition(definition)
    self.assertCharacterHasAttributeForDefinition(definition2)

  def testCorrectDefaultValueIsAssignedIfNotConcept(self):
    newAttributeDefinition = self.createAttrDefinition()
    self.character.addMissingCharacterAttributeDefinitions()
    expectedValue = newAttributeDefinition.default
    self.assertCharacterAttributeHasRawValue(newAttributeDefinition, expectedValue)

  def testAttributeValueIsConceptInstanceIdIfDefaultNamesValidConceptInstance(self):
    instance = self.createConceptInstance(concept = self.concept)
    newAttributeDefinition = self.createAttrDefinition(type = 'concept', concept=self.concept, default = instance.name)
    self.character.addMissingCharacterAttributeDefinitions()
    self.assertCharacterAttributeHasRawValue(newAttributeDefinition, instance.id)

  def testAttributeValueIsEmptyIfDefaultNamesInvalidConceptInstance(self):
    newAttributeDefinition = self.createAttrDefinition(type = 'concept', concept=self.concept, default = self.uniqStr())
    self.character.addMissingCharacterAttributeDefinitions()
    self.assertCharacterAttributeHasRawValue(newAttributeDefinition, '')

