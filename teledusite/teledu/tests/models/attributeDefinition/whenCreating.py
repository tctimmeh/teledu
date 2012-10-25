from teledu.models import CharacterAttributeDefinition, DataType
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreating(TeleduTestCase):
  def setUp(self):
    super(WhenCreating, self).setUp()
    self.definition = CharacterAttributeDefinition.objects.create(gameSystem = self.gameSystem, name = self.uniqStr())

  def testDefaultDataTypeIsText(self):
    self.assertTrue(self.definition.dataType.isText())

  def testDefaultValueConceptIsNull(self):
    self.assertIsNone(self.definition.valueConcept)

  def testDefinitionNotListByDefault(self):
    self.assertFalse(self.definition.list)

