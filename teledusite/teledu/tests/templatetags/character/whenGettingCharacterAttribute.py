from django.template import Context
from teledu.tests.teleduTestCase import TeleduTestCase
from teledu.models import GameSystem, CharacterAttributeDefinition
from teledu.templatetags.character import char_attr

class WhenEmbeddingCharacterAttribute(TeleduTestCase):
  def setUp(self):
    super(WhenEmbeddingCharacterAttribute, self).setUp()
    self.context = Context()
    self.context['character'] = self.character

  def assertCorrectAttributeElement(self, elementText, expectedAttributes = {}, definition = None):
    if definition is None:
      definition = self.charAttrDefn

    self.assertTrue(elementText.startswith('<span'))
    self.assertTrue(elementText.endswith('>%s</span>' % self.getCharacterAttributeValueByDefinition(definition)))
    self.assertIn('class="char_attr"', elementText)
    self.assertIn('id="attr_%d"' % definition.id, elementText)
    for attribute, value in expectedAttributes.items():
      self.assertIn('%s="%s"' % (attribute, value), elementText)

  def testThatAttributeElementIsReturnedUsingAttributeReference(self):
    actual = char_attr(self.context, self.charAttrDefn)
    self.assertCorrectAttributeElement(actual)

  def testThatAttributeElementIsReturnedUsingAttributeName(self):
    actual = char_attr(self.context, self.charAttrDefn.name)
    self.assertCorrectAttributeElement(actual)

  def testThatAttributeElementIsReturnedUsingAttributeNameAsUnicode(self):
    actual = char_attr(self.context, unicode(self.charAttrDefn.name))
    self.assertCorrectAttributeElement(actual)

  def testThatAttributeElementIsReturnedUsingAttributeNameWhenManyGameSystemsHaveSameAttributeName(self):
    gameSystem = GameSystem.objects.create(name = 'something else')
    CharacterAttributeDefinition.objects.create(gameSystem = gameSystem, name = self.charAttrDefn.name)

    actual = char_attr(self.context, self.charAttrDefn.name)
    self.assertCorrectAttributeElement(actual)

  def testThatDataInputAttributeIsSelectForConceptAttributes(self):
    definition = self.addAttrDefnToCharacter(type = 'concept')
    actual = char_attr(self.context, definition.name)
    self.assertCorrectAttributeElement(actual, expectedAttributes = {
      'data-editor': 'select'
    }, definition = definition)

