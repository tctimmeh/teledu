import random
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingValue(TeleduTestCase):
  def testThatIntegerAttributesAreReturnedAsInt(self):
    attribute = self.addAttributeToCharacter(type = 'integer', default = self.uniqInt())
    actual = self.getCharacterAttributeValueObject(attribute).value
    self.assertIsInstance(actual, int)

  def testThatRealAttributesAreReturnedAsFloat(self):
    attribute = self.addAttributeToCharacter(type = 'real', default = random.random())
    actual = self.getCharacterAttributeValueObject(attribute).value
    self.assertIsInstance(actual, float)

  def testThatConceptAttributesAreReturnedAsConceptInstanceName(self):
    conceptInstance = self.createConceptInstance()
    attribute = self.addAttributeToCharacter(type = 'concept', default = conceptInstance.id)
    actual = self.getCharacterAttributeValueObject(attribute).value
    self.assertEqual(actual, conceptInstance.name)

