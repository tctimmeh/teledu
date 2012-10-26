import random
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingCharacterAttribute(TeleduTestCase):
  def _createDependentAttribute(self, sourceAttribute, calcFunction):
    return self.addAttributeToCharacter(type = sourceAttribute.dataType, dependencies=[sourceAttribute],
      concept = sourceAttribute.valueConcept, calcFunction = calcFunction % {'sourceName': sourceAttribute.name})

  def _assertCalcFunctionProducesResult(self, sourceAttribute, calcFunction, expected):
    attribute = self._createDependentAttribute(sourceAttribute, calcFunction)
    attribute.calculateNewValue(self.character)
    actual = self.getCharacterAttributeValue(attribute)
    self.assertEqual(actual, expected)

  def testGettingTextAttributeReturnsAttributeValue(self):
    expected = self.getCharacterAttributeValue(self.charAttr)
    self._assertCalcFunctionProducesResult(self.charAttr, "result = character.%(sourceName)s", expected)

  def testGettingIntegerAttributeReturnsAttributeValue(self):
    expected = self.uniqInt()
    integerAttribute = self.addAttributeToCharacter(type = 'integer', default = expected - 1)
    self._assertCalcFunctionProducesResult(integerAttribute, "result = character.%(sourceName)s + 1", expected)

  def testGettingConceptAttributeReturnsConceptInstance(self):
    instance = self.createConceptInstance()
    conceptAttribute = self.addAttributeToCharacter(type = 'concept', concept = self.concept, default = instance.id)
    self._assertCalcFunctionProducesResult(conceptAttribute, "result = character.%(sourceName)s", instance.name)

