from django.core.exceptions import ObjectDoesNotExist
from teledu.models import Character, CharacterAttributeValue
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenDeletingCharacter(TeleduTestCase):
  def setUp(self):
    super(WhenDeletingCharacter, self).setUp()
    self.deleteUrl = '/character/%d/delete'

  def get(self):
    return self.client.get(self.deleteUrl % self.character.id)

  def post(self, data = {}):
    return self.client.post(self.deleteUrl % self.character.id, data, follow = True)

  def delete(self):
    return self.client.delete('/character/%d' % self.character.id, follow = True)

  def testThatURLReturnsSuccessCode(self):
    response = self.get()
    self.assertEqual(response.status_code, 200)

  def testThatDeleteCharacterTemplateIsRendered(self):
    response = self.get()
    self.assertTemplateUsed(response, "deleteCharacter.html")

  def testThatTemplateIsRenderedWithCharacter(self):
    response = self.get()
    actual = response.context[0].get('character', None)
    self.assertIsInstance(actual, Character)

  def testThatCharacterNotDeletedWhenConfirmNotSpecified(self):
    self.post()
    Character.objects.get(pk = self.character.id)

  def testThatPostingWithConfirmDeletesCharacter(self):
    self.post({'confirm': True})
    self.assertRaises(ObjectDoesNotExist, Character.objects.get, pk = self.character.id)

  def testThatCharacterAttributesAreDeletedWhenCharacterIsDeleted(self):
    self.post({'confirm': True})
    attributes = CharacterAttributeValue.objects.filter(character = self.character.id)
    self.assertEqual(len(attributes), 0)

  def testThatDeletingCharacterRedirectsToWelcomePage(self):
    response = self.post({'confirm': True})
    self.assertRedirects(response, '/')

  def testThatUsingDeleteMethodOnCharacterDeletesCharacter(self):
    self.delete()
    self.assertRaises(ObjectDoesNotExist, Character.objects.get, pk = self.character.id)

  def testThatGetWithBadIdReturns404(self):
    response = self.client.get(self.deleteUrl % self.uniqInt())
    self.assertEqual(response.status_code, 404)

  def testThatPostWithBadIdReturns404(self):
    response = self.client.post(self.deleteUrl % self.uniqInt())
    self.assertEqual(response.status_code, 404)

