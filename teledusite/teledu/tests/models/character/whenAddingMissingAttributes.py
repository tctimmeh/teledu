from teledu.tests.teleduTestCase import TeleduTestCase

class WhenAddingMissingAttributes(TeleduTestCase):
  def testAllMissingAttributesAreAdded(self):
    attribute = self.createAttribute()
    attribute2 = self.createAttribute()
    self.character.addMissingCharacterAttributes()
    self.assertCharacterHasAttributeValue(attribute)
    self.assertCharacterHasAttributeValue(attribute2)

  def testCorrectDefaultValueIsAssignedIfNotConcept(self):
    newAttribute = self.createAttribute()
    self.character.addMissingCharacterAttributes()
    expectedValue = newAttribute.default
    self.assertCharacterAttributeHasRawValue(newAttribute, expectedValue)

  def testAttributeValueIsConceptInstanceIdIfDefaultNamesValidConceptInstance(self):
    instance = self.createConceptInstance(concept = self.concept)
    newAttribute = self.createAttribute(type = 'concept', concept=self.concept, default = instance.name)
    self.character.addMissingCharacterAttributes()
    self.assertCharacterAttributeHasRawValue(newAttribute, instance.id)

  def testAttributeValueIsEmptyIfDefaultNamesInvalidConceptInstance(self):
    newAttribute = self.createAttribute(type = 'concept', concept=self.concept, default = self.uniqStr())
    self.character.addMissingCharacterAttributes()
    self.assertCharacterAttributeHasRawValue(newAttribute, '')

