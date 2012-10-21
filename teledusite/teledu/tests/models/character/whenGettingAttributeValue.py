from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingCharacterAttributeValue(TeleduTestCase):
  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeDefinitionId(self):
    actual = self.character.getAttributeValue(self.charAttrDefn.id)
    self.assertEqual(actual, self.charAttr.value)

  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeDefinition(self):
    actual = self.character.getAttributeValue(self.charAttrDefn)
    self.assertEqual(actual, self.charAttr.value)

  def testThatEmptyValueIsReturnedForConceptAttributeWithEmptyRawValue(self):
    definition = self.addAttrDefnToCharacter(type = 'concept', concept = self.concept)
    actual = self.character.getAttributeValue(definition)
    self.assertEqual(actual, '')

  def testThatListAttributesReturnListOfValues(self):
    self.charAttrDefn.list = True
    self.charAttrDefn.save()
    attr2 = self.createAttrForCharacter(self.charAttrDefn)
    expected = [self.charAttr.value, attr2.value]
    expected.sort()
    actual = self.character.getAttributeValue(self.charAttrDefn)
    actual.sort()
    self.assertEqual(actual, expected)

  def testThatListAttributesWithNoValuesReturnEmptyList(self):
    definition = self.createAttrDefinition(list = True)
    actual = self.character.getAttributeValue(definition)
    self.assertEqual(actual, [])

  def testThatListValuesAreReturnedAsCorrectTypes(self):
    definition = self.createAttrDefinition(type = 'integer', list = True)
    attr1 = self.createAttrForCharacter(definition, initialValue=self.uniqInt())
    attr2 = self.createAttrForCharacter(definition, initialValue=self.uniqInt())
    expected = [attr1.value, attr2.value]
    expected.sort()
    actual = self.character.getAttributeValue(definition)
    actual.sort()
    self.assertEquals(actual, expected)

