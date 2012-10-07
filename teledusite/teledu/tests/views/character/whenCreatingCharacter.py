from teledu.models import Character, CharacterAttribute
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreatingCharacter(TeleduTestCase):
  def testThatURLReturnsSuccessCode(self):
    response = self.client.get('/character')
    self.assertEqual(response.status_code, 200)

  def testThatCreateCharacterTemplateIsRendered(self):
    response = self.client.get('/character')
    self.assertTemplateUsed(response, "createCharacter.html")

  def testThatTemplateIsRenderedWithCharacterForm(self):
    response = self.client.get('/character')
    actual = response.context[0].get('form', None)
    self.assertIsNotNone(actual)

  def testThatFormIsRenderedWithDataWhenPostedDataIsInvalid(self):
    expected = self.uniqStr()
    response = self.client.post('/character', {'name' : expected})
    form = response.context['form']
    self.assertEqual(form.data['name'], expected)

  def testThatPostingValidDataCreatesNewCharacter(self):
    name = self.uniqStr()
    self.client.post('/character', {'name' : name, 'gameSystem': self.gameSystem.id}, follow = True)
    newCharacter = Character.objects.get(name = name)
    self.assertIsNotNone(newCharacter)

  def testThatPostingValidDataCreatesNewCharacterWithAttributesForGivenGameSystem(self):
    name = self.uniqStr()
    self.client.post('/character', {'name' : name, 'gameSystem': self.gameSystem.id}, follow = True)
    attributes = CharacterAttribute.objects.filter(character__name = name)
    self.assertGreater(len(attributes), 0)

  def testThatPostingValidDataRedirectsToCharacterSheet(self):
    name = self.uniqStr()
    response = self.client.post('/character', {'name' : name, 'gameSystem': self.gameSystem.id}, follow = True)
    newCharacter = Character.objects.get(name = name)
    self.assertRedirects(response, 'character/%d' % newCharacter.id)

