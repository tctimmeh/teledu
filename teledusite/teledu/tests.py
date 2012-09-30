"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .models import GameSystem, CharacterAttributeDefinition, Character, CharacterAttribute

class WhenGettingCharacterAttributeValue(TestCase):
  def setUp(self):
    self.gameSystem = GameSystem.objects.create(name = 'something')
    self.attrDefn = CharacterAttributeDefinition.objects.create(gameSystem = self.gameSystem, name = 'whatever')
    self.char = Character.objects.create(name = 'whomever')
    self.charAttr = CharacterAttribute.objects.create(character = self.char, attribute = self.attrDefn, value = 'a super value')

  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeId(self):
    actual = self.char.getAttribute(self.attrDefn.id)
    self.assertEqual(actual, self.charAttr.value)

  def testThatAttributeValueIsReturnedWhenSpecifyingAttributeDefinition(self):
    actual = self.char.getAttribute(self.attrDefn)
    self.assertEqual(actual, self.charAttr.value)

class WhenGettingCharacterGameSystem(TestCase):
  def setUp(self):
    self.gameSystem = GameSystem.objects.create(name = 'something')
    self.attrDefn = CharacterAttributeDefinition.objects.create(gameSystem = self.gameSystem, name = 'whatever')
    self.char = Character.objects.create(name = 'whomever')
    self.charAttr = CharacterAttribute.objects.create(character = self.char, attribute = self.attrDefn, value = 'a super value')

  def testThatCorrectGameSystemIsReturned(self):
    actual = self.char.gameSystem
    self.assertEqual(actual, self.gameSystem)
