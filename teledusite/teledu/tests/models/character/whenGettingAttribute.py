from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingCharacterAttributeValue(TeleduTestCase):
  def testThatAttributeIsReturnedWhenSpecifyingAttributeDefinitionId(self):
    actual = self.character.getAttributeByDefinition(self.attributeDefinition.id)
    self.assertEqual(actual, self.charAttr)

  def testThatAttributeIsReturnedWhenSpecifyingAttributeDefinition(self):
    actual = self.character.getAttributeByDefinition(self.attributeDefinition)
    self.assertEqual(actual, self.charAttr)

