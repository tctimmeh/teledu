from teledu.models import CharacterAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreating(TeleduTestCase):
  def setUp(self):
    super(WhenCreating, self).setUp()
    self.attribute = CharacterAttribute.objects.create(gameSystem = self.gameSystem, name = self.uniqStr())

  def testDefaultDisplayValueIsTrue(self):
    self.assertTrue(self.attribute.display)

  def testDefaultAttributeValueIsBlank(self):
    self.assertEqual(self.attribute.default, '')

  def testDefaultCalcFunctionIsNull(self):
    self.assertIsNone(self.attribute.calcFunction, None)
