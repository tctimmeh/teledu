from teledu.models import CharacterAttributeDefinition
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreatingCharacterAttributeDefinition(TeleduTestCase):
  def setUp(self):
    super(WhenCreatingCharacterAttributeDefinition, self).setUp()
    self.definition = CharacterAttributeDefinition.objects.create(gameSystem = self.gameSystem, name = self.uniqStr())

  def testDefaultDisplayValueIsTrue(self):
    self.assertTrue(self.definition.display)

  def testDefaultAttributeValueIsBlank(self):
    self.assertEqual(self.definition.default, '')

  def testDefaultCalcFunctionIsNull(self):
    self.assertIsNone(self.definition.calcFunction, None)
