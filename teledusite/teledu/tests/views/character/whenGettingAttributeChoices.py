import json
from django.http import HttpResponseNotFound
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingAttributeChoices(TeleduTestCase):
  def _getChoices(self, attribute):
    response = self.client.get('/character/%d/attribute/%d/choices' % (self.character.id, attribute.id))
    return response

  def testThatMapOfConceptInstancesIsReturnedForConceptAttributes(self):
    instance1 = self.createConceptInstance(concept = self.concept)
    instance2 = self.createConceptInstance(concept = self.concept)
    attribute = self.addAttributeToCharacter(type = 'concept', concept = self.concept, default = instance2.id)

    expected = {str(instance1.id): instance1.name, str(instance2.id): instance2.name, 'selected': str(instance2.id)}
    response = self._getChoices(attribute)
    actual = json.loads(response.content)
    self.assertEqual(actual, expected)

  def testThatEmptyResponseIsReturnedForTextAttributes(self):
    response = self._getChoices(self.charAttr)
    self.assertEqual(response.content, '')

  def testThat404IsReturnedForBadCharacterId(self):
    response = self.client.get('/character/%d/attribute/%d/choices' % (self.uniqInt(), self.charAttr.id))
    self.assertIsInstance(response, HttpResponseNotFound)

  def testThat404IsReturnedForBadAttributeId(self):
    response = self.client.get('/character/%d/attribute/%d/choices' % (self.character.id, self.uniqInt()))
    self.assertEqual(response.status_code, 404)

