import random
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingValue(TeleduTestCase):
  def testThatIntegerAttributesAreReturnedAsInt(self):
    definition = self.addAttrDefnToCharacter(type = 'integer', default = self.uniqInt())
    actual = self.getCharacterAttributeForDefinition(definition).value
    self.assertIsInstance(actual, int)

  def testThatRealAttributesAreReturnedAsFloat(self):
    definition = self.addAttrDefnToCharacter(type = 'real', default = random.random())
    actual = self.getCharacterAttributeForDefinition(definition).value
    self.assertIsInstance(actual, float)

  def testThatConceptAttributesAreReturnedAsConceptInstanceName(self):
    conceptInstance = self.createConceptInstance()
    definition = self.addAttrDefnToCharacter(type = 'concept', default = conceptInstance.id)
    actual = self.getCharacterAttributeForDefinition(definition).value
    self.assertEqual(actual, conceptInstance.name)

