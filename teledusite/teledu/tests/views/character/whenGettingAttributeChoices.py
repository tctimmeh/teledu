import json
from django.http import HttpResponseNotFound
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingAttributeChoices(TeleduTestCase):
  def _getChoices(self, definition):
    response = self.client.get('/character/%d/attribute/%d/choices' % (self.character.id, definition.id))
    return response

  def testThatMapOfConceptInstancesIsReturnedForConceptAttributes(self):
    instance1 = self.createConceptInstance(concept = self.concept)
    instance2 = self.createConceptInstance(concept = self.concept)
    definition = self.addAttrDefnToCharacter(type = 'concept', concept = self.concept, default = instance2.id)

    expected = {str(instance1.id): instance1.name, str(instance2.id): instance2.name, 'selected': str(instance2.id)}
    response = self._getChoices(definition)
    actual = json.loads(response.content)
    self.assertEqual(actual, expected)

  def testThatEmptyResponseIsReturnedForTextAttributes(self):
    response = self._getChoices(self.charAttrDefn)
    self.assertEqual(response.content, '')

  def testThat404IsReturnedForBadCharacterId(self):
    response = self.client.get('/character/%d/attribute/%d/choices' % (self.uniqInt(), self.charAttrDefn.id))
    self.assertIsInstance(response, HttpResponseNotFound)

  def testThat404IsReturnedForBadAttributeId(self):
    response = self.client.get('/character/%d/attribute/%d/choices' % (self.character.id, self.uniqInt()))
    self.assertEqual(response.status_code, 404)

