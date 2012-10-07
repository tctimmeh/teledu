import random
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingCharacterAttributeValue(TeleduTestCase):
  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeDefinitionId(self):
    actual = self.character.getAttributeValueByDefinition(self.attributeDefinition.id)
    self.assertEqual(actual, self.charAttr.value)

  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeDefinition(self):
    actual = self.character.getAttributeValueByDefinition(self.attributeDefinition)
    self.assertEqual(actual, self.charAttr.value)

  def testThatIntegerAttributesAreReturnedAsInt(self):
    definition = self.addAttrDefinition(type = 'integer', default = self.uniqInt())
    actual = self.character.getAttributeValueByDefinition(definition)
    self.assertIsInstance(actual, int)

  def testThatRealAttributesAreReturnedAsFloat(self):
    definition = self.addAttrDefinition(type = 'real', default = random.random())
    actual = self.character.getAttributeValueByDefinition(definition)
    self.assertIsInstance(actual, float)

