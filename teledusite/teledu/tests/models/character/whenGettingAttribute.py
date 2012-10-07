from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingCharacterAttribute(TeleduTestCase):
  def testThatAttributeIsReturnedWhenSpecifyingAttributeDefinitionId(self):
    actual = self.character.getAttributeByDefinition(self.attributeDefinition.id)
    self.assertEqual(actual, self.charAttr)

  def testThatAttributeIsReturnedWhenSpecifyingAttributeDefinition(self):
    actual = self.character.getAttributeByDefinition(self.attributeDefinition)
    self.assertEqual(actual, self.charAttr)

  def testThatAttributesAreSortedByNameWhenGettingByName(self):
    attr2 = self.addAttrDefinition(name = 'A' + self.uniqStr())
    expected = [self.attributeDefinition, attr2]
    expected.sort(lambda a, b: cmp(a.name, b.name))

    actual = self.character.attributesByName()
    self.assertEqual(list(actual), expected)

