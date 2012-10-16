from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingSimpleValue(TeleduTestCase):
  def _calculateAttrFunctionForDefinition(self, definition):
    calculatedDefinition = self.addAttrDefnToCharacter(calcFunction = "result = attr('%s')" % definition.name)
    attribute = self.getCharacterAttributeForDefinition(calculatedDefinition)
    return attribute.calculateNewValue()

  def testGettingTextAttributeReturnsAttributeValueAsString(self):
    sourceDefinition = self.addAttrDefnToCharacter(default = self.uniqStr())
    expected = self.getCharacterAttributeValueByDefinition(sourceDefinition)

    actual = self._calculateAttrFunctionForDefinition(sourceDefinition)
    self.assertEqual(actual, expected)

  def testGettingIntegerAttributeReturnsAttributeValueAsInt(self):
    sourceDefinition = self.addAttrDefnToCharacter(type = 'integer', default = self.uniqInt())
    expected = self.getCharacterAttributeValueByDefinition(sourceDefinition)

    actual = self._calculateAttrFunctionForDefinition(sourceDefinition)
    self.assertEqual(actual, expected)
    self.assertIsInstance(actual, int)

  def testGettingConceptAttributeReturnsAttributeValueConceptName(self):
    conceptInstance = self.createConceptInstance()
    sourceDefinition = self.addAttrDefnToCharacter(type = 'concept', default = conceptInstance.id)
    expected = conceptInstance.name

    actual = self._calculateAttrFunctionForDefinition(sourceDefinition)
    self.assertEqual(actual, expected)

