import random
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenViewingCharacterSheet(TeleduTestCase):
  def setUp(self):
    super(WhenViewingCharacterSheet, self).setUp()
    self.response = self.client.get('/character/%d' % self.character.id)

  def testThatSuccessCodeIsReturnedForValidCharacterId(self):
    self.assertEqual(self.response.status_code, 200)

  def testThatNotFoundCodeIsReturnedForInvalidCharacterId(self):
    self.response = self.client.get('/character/%d' % self.uniqInt())
    self.assertEqual(self.response.status_code, 404)

  def testThatBaseCharacterSheetTemplateIsRendered(self):
    self.assertTemplateUsed(self.response, 'characterSheet.html')

  def testThatCustomTemplateIsRenderedInOutput(self):
    self.assertContains(self.response, self.charSheetTemplate.template)

  def testThatDefaultTemplateIsRenderedWhenNoCustomTemplateIsAvailable(self):
    self.charSheetTemplate.delete()
    self.response = self.client.get('/character/%d' % self.character.id)

  def testThatRenderedContextContainsCharacter(self):
    self.assertEqual(self.response.context['character'], self.character)

