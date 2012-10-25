from teledu.models import CharacterAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreating(TeleduTestCase):
  def setUp(self):
    super(WhenCreating, self).setUp()
    self.definition = CharacterAttribute.objects.create(gameSystem = self.gameSystem, name = self.uniqStr())

  def testDefaultDisplayValueIsTrue(self):
    self.assertTrue(self.definition.display)

  def testDefaultAttributeValueIsBlank(self):
    self.assertEqual(self.definition.default, '')

  def testDefaultCalcFunctionIsNull(self):
    self.assertIsNone(self.definition.calcFunction, None)
