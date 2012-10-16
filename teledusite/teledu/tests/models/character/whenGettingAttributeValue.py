from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingCharacterAttributeValue(TeleduTestCase):
  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeDefinitionId(self):
    actual = self.character.getAttributeValueByDefinition(self.charAttrDefn.id)
    self.assertEqual(actual, self.charAttr.value)

  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeDefinition(self):
    actual = self.character.getAttributeValueByDefinition(self.charAttrDefn)
    self.assertEqual(actual, self.charAttr.value)

  def testThatEmptyValueIsReturnedForConceptAttributeWithEmptyRawValue(self):
    definition = self.addAttrDefnToCharacter(type = 'concept', concept = self.concept)
    actual = self.character.getAttributeValueByDefinition(definition)
    self.assertEqual(actual, '')
