from teledu.tests.teleduTestCase import TeleduTestCase

class WhenSettingValue(TeleduTestCase):
  def testStringValueCreatesCorrectAttributeValue(self):
    expected = self.uniqStr()
    attribute = self.addAttributeToCharacter(type = "text")
    attribute.setValue(self.character, expected)
    actual = attribute.getValue(self.character)
    self.assertEqual(actual, expected)

  def testIntegerValueCreatesCorrectAttributeValue(self):
    expected = self.uniqInt()
    attribute = self.addAttributeToCharacter(type = "integer")
    attribute.setValue(self.character, expected)
    actual = attribute.getValue(self.character)
    self.assertEqual(actual, expected)

  def testListCreatesCorrectAttributeValues(self):
    expected = [1,2,3]
    attribute = self.addAttributeToCharacter(type = "integer", list = True)
    attribute.setValue(self.character, expected)
    actual = attribute.getValue(self.character)
    self.assertEqual(actual, expected)

