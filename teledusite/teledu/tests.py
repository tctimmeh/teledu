"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.template import Context

from django.test import TestCase
from .models import GameSystem, CharacterAttributeDefinition, Character, CharacterAttribute
from .templatetags.character import char_attr

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

class WhenEmbeddingCharacterAttribute(TestCase):
  def setUp(self):
    self.gameSystem = GameSystem.objects.create(name = 'something')
    self.attrDefn = CharacterAttributeDefinition.objects.create(gameSystem = self.gameSystem, name = 'whatever')
    self.char = Character.objects.create(name = 'whomever')
    self.attributeValue = 'a testing value'
    self.charAttr = CharacterAttribute.objects.create(character = self.char, attribute = self.attrDefn, value = self.attributeValue)
    self.context = Context()
    self.context['character'] = self.char

  def assertCorrectAttributeElement(self, elementText):
    self.assertEqual(elementText, '<span id="attr_%d">%s</span>' % (self.attrDefn.id, self.attributeValue))

  def testThatAttributeElementIsReturnedUsingAttributeReference(self):
    actual = char_attr(self.context, self.attrDefn)
    self.assertCorrectAttributeElement(actual)

  def testThatAttributeElementIsReturnedUsingAttributeName(self):
    actual = char_attr(self.context, self.attrDefn.name)
    self.assertCorrectAttributeElement(actual)

  def testThatAttributeElementIsReturnedUsingAttributeNameAsUnicode(self):
    actual = char_attr(self.context, unicode(self.attrDefn.name))
    self.assertCorrectAttributeElement(actual)

  def testThatAttributeElementIsReturnedUsingAttributeNameWhenManyGameSystemsHaveSameAttributeName(self):
    gameSystem = GameSystem.objects.create(name = 'something else')
    CharacterAttributeDefinition.objects.create(gameSystem = gameSystem, name = self.attrDefn.name)

    actual = char_attr(self.context, self.attrDefn.name)
    self.assertCorrectAttributeElement(actual)

