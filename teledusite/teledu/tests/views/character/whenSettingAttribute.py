import random
from teledu.models import CharacterAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenSettingAttribute(TeleduTestCase):
  def setUp(self):
    super(WhenSettingAttribute, self).setUp()
    self.newValue = self.uniqStr()
    self.response = self._doRequest(value = self.newValue)

  def _doRequest(self, value = None, characterId = None, attributeId = None):
    if characterId is None:
      characterId = self.character.id
    if attributeId is None:
      attributeId = self.attributeDefinition.id
    if value is None:
      value = self.uniqStr()

    return self.client.post('/character/%d/attribute/%d' % (characterId, attributeId), {
      'value': value
    })

  def testThatSuccessCodeIsReturnedForValidAttributeId(self):
    self.assertEqual(self.response.status_code, 200)

  def testThatNotFoundCodeIsReturnedForInvalidCharacterId(self):
    self.response = self._doRequest(characterId = random.randint(999999, 99999999))
    self.assertEqual(self.response.status_code, 404)

  def testThatNotFoundCodeIsReturnedForInvalidAttributeId(self):
    self.response = self._doRequest(attributeId = random.randint(999999, 99999999))
    self.assertEqual(self.response.status_code, 404)

  def testThatAttributeGetsNewValue(self):
    actual = CharacterAttribute.objects.get(pk = self.charAttr.id).raw_value
    self.assertEqual(actual, self.newValue)

  def testThatResponseContainsNewValue(self):
    self.assertEqual(self.response.content, self.newValue)

