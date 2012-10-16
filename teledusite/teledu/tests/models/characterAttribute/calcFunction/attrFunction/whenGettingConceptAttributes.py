from teledu.models import ConceptInstanceAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingConceptAttributes(TeleduTestCase):
  def testGettingAttributeOfConceptReturnsConceptInstanceValue(self):
    expected = self.uniqStr()
    conceptInstance = self.createConceptInstance(attributes = {self.conceptAttrDefn: expected})
    sourceDefinition = self.addAttrDefnToCharacter(type = 'concept', concept = self.concept, default = conceptInstance.id)

    calculatedDefinition = self.addAttrDefnToCharacter(calcFunction = "result = attr('%s.%s')" % (sourceDefinition.name, self.conceptAttrDefn.name))
    attribute = self.getCharacterAttributeForDefinition(calculatedDefinition)
    actual = attribute.calculateNewValue()

    self.assertEqual(actual, expected)

