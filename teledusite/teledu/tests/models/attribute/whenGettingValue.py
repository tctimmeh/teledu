import random
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingValue(TeleduTestCase):
  def testThatIntegerAttributesAreReturnedAsInt(self):
    attribute = self.addAttributeToCharacter(type = 'integer', default = self.uniqInt())
    actual = self.getCharacterAttributeValueObject(attribute).value
    self.assertIsInstance(actual, int)

  def testThatRealAttributesAreReturnedAsFloat(self):
    attribute = self.addAttributeToCharacter(type = 'real', default = random.random())
    actual = self.getCharacterAttributeValueObject(attribute).value
    self.assertIsInstance(actual, float)

  def testThatConceptAttributesAreReturnedAsConceptInstanceName(self):
    conceptInstance = self.createConceptInstance()
    attribute = self.addAttributeToCharacter(type = 'concept', default = conceptInstance.id)
    actual = self.getCharacterAttributeValueObject(attribute).value
    self.assertEqual(actual, conceptInstance.name)

  def testThatEmptyValueIsReturnedForConceptAttributeWithEmptyRawValue(self):
    attribute = self.addAttributeToCharacter(type = 'concept', concept = self.concept)
    actual = self.character.getAttributeValue(attribute)
    self.assertEqual(actual, '')

  def testThatConceptInstanceNameIsReturnedForConceptAttributeWithValidConceptId(self):
    instance = self.createConceptInstance()
    attribute = self.addAttributeToCharacter(type = 'concept', concept = self.concept, default = instance.id)
    actual = self.character.getAttributeValue(attribute)
    self.assertEqual(actual, instance.name)

  def testThatListAttributesReturnListOfValues(self):
    self.charAttr.list = True
    self.charAttr.save()
    attr2 = self.createAttributeValueForCharacter(self.charAttr)
    expected = [self.charAttrValue.value, attr2.value]
    expected.sort()
    actual = self.character.getAttributeValue(self.charAttr)
    actual.sort()
    self.assertEqual(actual, expected)

  def testThatListAttributesWithNoValuesReturnEmptyList(self):
    attribute = self.createAttribute(list = True)
    actual = self.character.getAttributeValue(attribute)
    self.assertEqual(actual, [])

  def testThatListValuesAreReturnedAsCorrectTypes(self):
    attribute = self.createAttribute(type = 'integer', list = True)
    attr1 = self.createAttributeValueForCharacter(attribute, initialValue=self.uniqInt())
    attr2 = self.createAttributeValueForCharacter(attribute, initialValue=self.uniqInt())
    expected = [attr1.value, attr2.value]
    expected.sort()
    actual = self.character.getAttributeValue(attribute)
    actual.sort()
    self.assertEquals(actual, expected)

