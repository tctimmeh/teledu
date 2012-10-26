from teledu.models import CharacterAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreating(TeleduTestCase):
  def setUp(self):
    super(WhenCreating, self).setUp()
    self.attribute = CharacterAttribute.objects.create(gameSystem = self.gameSystem, name = self.uniqStr())

  def testDefaultDataTypeIsText(self):
    self.assertTrue(self.attribute.dataType.isText())

  def testDefaultValueConceptIsNull(self):
    self.assertIsNone(self.attribute.valueConcept)

  def testAttributeNotListByDefault(self):
    self.assertFalse(self.attribute.list)

