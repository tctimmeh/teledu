from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingSimpleValue(TeleduTestCase):
  def _executeCalcFunctionForAttribute(self, attribute):
    calculatedAttribute = self.addAttributeToCharacter(calcFunction = "result = attr('%s')" % attribute.name)
    return calculatedAttribute.calculateNewValue(self.character)

  def testGettingTextAttributeReturnsAttributeValueAsString(self):
    sourceAttribute = self.addAttributeToCharacter(default = self.uniqStr())
    expected = self.getCharacterAttributeValue(sourceAttribute)

    actual = self._executeCalcFunctionForAttribute(sourceAttribute)
    self.assertEqual(actual, expected)

  def testGettingIntegerAttributeReturnsAttributeValueAsInt(self):
    sourceAttribute = self.addAttributeToCharacter(type = 'integer', default = self.uniqInt())
    expected = self.getCharacterAttributeValue(sourceAttribute)

    actual = self._executeCalcFunctionForAttribute(sourceAttribute)
    self.assertEqual(actual, expected)
    self.assertIsInstance(actual, int)

  def testGettingConceptAttributeReturnsAttributeValueConceptName(self):
    conceptInstance = self.createConceptInstance()
    sourceAttribute = self.addAttributeToCharacter(type = 'concept', default = conceptInstance.id)
    expected = conceptInstance.name

    actual = self._executeCalcFunctionForAttribute(sourceAttribute)
    self.assertEqual(actual, expected)

  def testGettingListAttributeReturnsAllAttributesAsList(self):
    attribute = self.createAttribute(list = True)
    attr1 = self.createAttributeValueForCharacter(attribute, initialValue = self.uniqStr())
    attr2 = self.createAttributeValueForCharacter(attribute, initialValue = self.uniqStr())
    expected = [attr1.value, attr2.value]
    expected.sort()

    actual = self._executeCalcFunctionForAttribute(attribute)
    actual.sort()
    self.assertEqual(actual, expected)

