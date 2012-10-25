from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingConceptAttributes(TeleduTestCase):
  def testGettingAttributeOfConceptReturnsConceptInstanceValue(self):
    expected = self.uniqStr()
    conceptInstance = self.createConceptInstance(attributes = {self.conceptAttr: expected})
    sourceAttribute = self.addAttributeToCharacter(type = 'concept', concept = self.concept, default = conceptInstance.id)

    calculatedAttribute = self.addAttributeToCharacter(calcFunction = "result = attr('%s.%s')" % (sourceAttribute.name, self.conceptAttr.name))
    actual = calculatedAttribute.calculateNewValue(self.character)

    self.assertEqual(actual, expected)

