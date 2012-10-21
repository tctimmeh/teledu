from django.template import Context
from teledu.tests.teleduTestCase import TeleduTestCase
from teledu.models import GameSystem, CharacterAttributeDefinition
from teledu.templatetags.character import createAttributeElement

class WhenEmbeddingCharacterAttribute(TeleduTestCase):
  def setUp(self):
    super(WhenEmbeddingCharacterAttribute, self).setUp()
    self.context = Context()
    self.context['character'] = self.character

  def assertElementAttributes(self, definition, elementText, expectedAttributes):
    self.assertIn('class="char_attr"', elementText)
    self.assertIn('id="attr_%d"' % definition.id, elementText)
    if expectedAttributes:
      for attribute, value in expectedAttributes.items():
        self.assertIn('%s="%s"' % (attribute, value), elementText)

  def assertElementForSimpleAttribute(self, elementText, expectedAttributes = None, definition = None):
    if definition is None:
      definition = self.charAttrDefn

    self.assertTrue(elementText.startswith('<span'))
    self.assertTrue(elementText.endswith('>%s</span>' % self.getCharacterAttributeValueByDefinition(definition)))
    self.assertElementAttributes(definition, elementText, expectedAttributes)

  def assertElementForListAttribute(self, elementText, items, expectedAttributes = None, definition = None):
    if definition is None:
      definition = self.charAttrDefn

    self.assertTrue(elementText.startswith('<ul'))
    self.assertTrue(elementText.endswith('</ul>'))
    self.assertElementAttributes(definition, elementText, expectedAttributes)
    for item in items:
      self.assertIn('<li>%s</li>' % item, elementText)

  def testThatAttributeElementIsReturnedUsingAttributeReference(self):
    actual = createAttributeElement(self.context, self.charAttrDefn)
    self.assertElementForSimpleAttribute(actual)

  def testThatAttributeElementIsReturnedUsingAttributeName(self):
    actual = createAttributeElement(self.context, self.charAttrDefn.name)
    self.assertElementForSimpleAttribute(actual)

  def testThatAttributeElementIsReturnedUsingAttributeNameAsUnicode(self):
    actual = createAttributeElement(self.context, unicode(self.charAttrDefn.name))
    self.assertElementForSimpleAttribute(actual)

  def testThatAttributeElementIsReturnedUsingAttributeNameWhenManyGameSystemsHaveSameAttributeName(self):
    gameSystem = GameSystem.objects.create(name = 'something else')
    CharacterAttributeDefinition.objects.create(gameSystem = gameSystem, name = self.charAttrDefn.name)

    actual = createAttributeElement(self.context, self.charAttrDefn.name)
    self.assertElementForSimpleAttribute(actual)

  def testThatDataInputAttributeIsSelectForConceptAttributes(self):
    definition = self.addAttrDefnToCharacter(type = 'concept')
    actual = createAttributeElement(self.context, definition.name)
    self.assertElementForSimpleAttribute(actual, expectedAttributes = {
      'data-editor': 'select'
    }, definition = definition)

  def testThatListElementIsReturnedForListAttributes(self):
    definition = self.createAttrDefinition(list = True)
    attr1 = self.createAttrForCharacter(definition, initialValue = self.uniqStr())
    attr2 = self.createAttrForCharacter(definition, initialValue = self.uniqStr())
    actual = createAttributeElement(self.context, definition)
    self.assertElementForListAttribute(actual, [attr1.value, attr2.value], definition = definition)

