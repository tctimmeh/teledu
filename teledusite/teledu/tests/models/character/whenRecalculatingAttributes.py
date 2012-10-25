from teledu.models import CharacterAttributeValue
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenRecalculatingAttributes(TeleduTestCase):
  def testThatAllAttributesAreRecalculated(self):
    expected = self.uniqStr()
    attr = self.addAttributeToCharacter(dependencies=[self.charAttr], calcFunction='result = "%s"' % expected)
    attr2 = self.addAttributeToCharacter(dependencies=[attr], calcFunction='result = "%s"' % expected)

    self.character.recalculateAllAttributes()
    actual = CharacterAttributeValue.objects.get(character = self.character, attribute = attr).value
    self.assertEqual(actual, expected)
    actual = CharacterAttributeValue.objects.get(character = self.character, attribute = attr2).value
    self.assertEqual(actual, expected)
