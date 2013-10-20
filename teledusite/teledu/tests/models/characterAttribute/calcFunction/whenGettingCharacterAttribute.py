from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingCharacterAttribute(TeleduTestCase):
  def _createDependentAttribute(self, sourceAttribute, calcFunction, type = None, list = False):
    if type is None:
      type = sourceAttribute.dataType

    return self.addAttributeToCharacter(type = type, dependencies=[sourceAttribute],
      concept = sourceAttribute.valueConcept, calcFunction = calcFunction % {'sourceName': sourceAttribute.name},
      list = list)

  def _assertCalcFunctionProducesResult(self, sourceAttribute, calcFunction, expected, type = None):
    isList = False
    if isinstance(expected, list):
      isList = True

    attribute = self._createDependentAttribute(sourceAttribute, calcFunction, type = type, list = isList)
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

  def testGettingAttributeOfConceptValueReturnsConceptAttributeValue(self):
    conceptAttr = self.createConceptAttr(type = 'concept', valueConcept = self.concept)
    expectedInstance = self.createConceptInstance()
    instance = self.createConceptInstance(attributes = {conceptAttr: expectedInstance.id})

    attribute = self.addAttributeToCharacter(type = 'concept', concept = self.concept, default = instance.id)
    self._assertCalcFunctionProducesResult(attribute,
      "result = character.%s.%s" % (attribute.name, conceptAttr.name),
      expectedInstance.name)

  def testIndexingListAttributeReturnsListElement(self):
    expected = self.uniqStr()
    attribute = self.createAttribute(list = True)
    self.createAttributeValueForCharacter(attribute)
    self.createAttributeValueForCharacter(attribute, initialValue=expected)
    self.createAttributeValueForCharacter(attribute)

    self._assertCalcFunctionProducesResult(attribute, "result = character.%(sourceName)s[1]", expected)

  def testGettingAttributeOfConceptInstanceFromListAttributeReturnsInstanceAttributeValue(self):
    expected = self.uniqStr()
    conceptAttr = self.createConceptAttr()

    attribute = self.createAttribute(list = True, type = 'concept', concept = self.concept)
    self.createAttributeValueForCharacter(attribute, initialValue = self.createConceptInstance().id)
    self.createAttributeValueForCharacter(attribute, initialValue = self.createConceptInstance(attributes = {conceptAttr: expected}).id)
    self.createAttributeValueForCharacter(attribute, initialValue = self.createConceptInstance().id)

    self._assertCalcFunctionProducesResult(attribute,
      "result = character.%s[1].%s" % (attribute.name, conceptAttr.name),
      expected, type = 'text')

  def testReturningListOfValuesSetsListAttribute(self):
    attribute = self.createAttribute(list = True)
    expected = [self.uniqStr(), self.uniqStr(), self.uniqStr()]
    self._assertCalcFunctionProducesResult(attribute, "result = %s" % expected, expected)
