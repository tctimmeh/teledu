from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingCharacterAttributeValue(TeleduTestCase):
  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeId(self):
    actual = self.character.getAttributeValue(self.charAttr.id)
    self.assertEqual(actual, self.charAttrValue.value)

  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeObject(self):
    actual = self.character.getAttributeValue(self.charAttr)
    self.assertEqual(actual, self.charAttrValue.value)

  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeName(self):
    actual = self.character.getAttributeValue(self.charAttr.name)
    self.assertEqual(actual, self.charAttrValue.value)

