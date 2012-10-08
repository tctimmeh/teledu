from teledu.models import CharacterAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenRecalculatingAttributes(TeleduTestCase):
  def testThatAllAttributesAreRecalculated(self):
    expected = self.uniqStr()
    attr = self.addAttrDefinition(dependencies=[self.attributeDefinition], calcFunction='result = "%s"' % expected)
    attr2 = self.addAttrDefinition(dependencies=[attr], calcFunction='result = "%s"' % expected)

    self.character.recalculateAllAttributes()
    actual = CharacterAttribute.objects.get(character = self.character, definition = attr).value
    self.assertEqual(actual, expected)
    actual = CharacterAttribute.objects.get(character = self.character, definition = attr2).value
    self.assertEqual(actual, expected)
