import random
from teledu.models import CharacterAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingValue(TeleduTestCase):
  def testThatIntegerAttributesAreReturnedAsInt(self):
    definition = self.createAttrDefinition(type = 'integer', default = self.uniqInt())
    attribute = self.createAttrForCharacter(definition)
    attribute = CharacterAttribute.objects.get(pk = attribute.id)

    actual = attribute.value
    self.assertIsInstance(actual, int)

  def testThatRealAttributesAreReturnedAsFloat(self):
    definition = self.createAttrDefinition(type = 'real', default = random.random())
    attribute = self.createAttrForCharacter(definition)
    attribute = CharacterAttribute.objects.get(pk = attribute.id)

    actual = attribute.value
    self.assertIsInstance(actual, float)

