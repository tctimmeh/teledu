from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingSimpleValue(TeleduTestCase):
  def _calculateAttrFunctionForDefinition(self, definition):
    calculatedDefinition = self.addAttrDefnToCharacter(calcFunction = "result = attr('%s')" % definition.name)
    return calculatedDefinition.calculateNewValue(self.character)

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

  def testGettingListAttributeReturnsAllAttributesAsList(self):
    definition = self.createAttrDefinition(list = True)
    attr1 = self.createAttrForCharacter(definition, initialValue = self.uniqStr())
    attr2 = self.createAttrForCharacter(definition, initialValue = self.uniqStr())
    expected = [attr1.value, attr2.value]
    expected.sort()

    actual = self._calculateAttrFunctionForDefinition(definition)
    actual.sort()
    self.assertEqual(actual, expected)

