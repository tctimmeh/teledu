import json
from teledu.models import  CharacterAttributeValue
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
      attributeId = self.charAttr.id
    if value is None:
      value = self.uniqStr()

    return self.client.post('/character/%d/attribute/%d' % (characterId, attributeId), {
      'value': value
    })

  def testThatSuccessCodeIsReturnedForValidAttributeId(self):
    self.assertEqual(self.response.status_code, 200)

  def testThatNotFoundCodeIsReturnedForInvalidCharacterId(self):
    self.response = self._doRequest(characterId = self.uniqInt())
    self.assertEqual(self.response.status_code, 404)

  def testThatNotFoundCodeIsReturnedForInvalidAttributeId(self):
    self.response = self._doRequest(attributeId = self.uniqInt())
    self.assertEqual(self.response.status_code, 404)

  def testThatAttributeGetsNewValue(self):
    actual = CharacterAttributeValue.objects.get(pk = self.charAttrValue.id).raw_value
    self.assertEqual(actual, self.newValue)

  def testThatResponseContainsJsonObjectOfEveryChangedAttribute(self):
    dependentAttribute = self.addAttributeToCharacter(dependencies=[self.charAttr], default = self.uniqStr())

    value = self.uniqStr()
    response = self._doRequest(value = value)
    expected = json.dumps({
      self.charAttr.id: value,
      dependentAttribute.id: self.getCharacterAttributeValue(dependentAttribute),
    })
    actual = response.content
    self.assertEqual(actual, expected)

  def testThatResponseContainsConceptInstanceNames(self):
    instance1 = self.createConceptInstance(concept = self.concept)
    instance2 = self.createConceptInstance(concept = self.concept)
    changeAttribute = self.addAttributeToCharacter(type = 'concept', concept = self.concept, default = instance1.id)
    dependentAttribute = self.addAttributeToCharacter(dependencies = [changeAttribute], type = 'concept', concept = self.concept, default = instance1.id)

    response = self._doRequest(value = instance2.id, attributeId = changeAttribute.id)
    expected = json.dumps({
      changeAttribute.id: self.getCharacterAttributeValue(changeAttribute),
      dependentAttribute.id: self.getCharacterAttributeValue(dependentAttribute),
    })
    actual = response.content
    self.assertEqual(actual, expected)
