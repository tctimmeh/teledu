from django.template import Context
from teledu.tests.teleduTestCase import TeleduTestCase
from teledu.models import GameSystem, CharacterAttribute
from teledu.templatetags.character import createAttributeElement

class WhenEmbeddingCharacterAttribute(TeleduTestCase):
  def setUp(self):
    super(WhenEmbeddingCharacterAttribute, self).setUp()
    self.context = Context()
    self.context['character'] = self.character

  def assertElementAttributes(self, attribute, elementText, expectedAttributes):
    self.assertIn('class="char_attr"', elementText)
    self.assertIn('id="attr_%d"' % attribute.id, elementText)
    if expectedAttributes:
      for attribute, value in expectedAttributes.items():
        self.assertIn('%s="%s"' % (attribute, value), elementText)

  def assertElementForSimpleAttribute(self, elementText, expectedAttributes = None, attribute = None):
    if attribute is None:
      attribute = self.charAttr

    self.assertTrue(elementText.startswith('<span'))
    self.assertTrue(elementText.endswith('>%s</span>' % self.getCharacterAttributeValue(attribute)))
    self.assertElementAttributes(attribute, elementText, expectedAttributes)

  def assertElementForListAttribute(self, elementText, items, expectedAttributes = None, attribute = None):
    if attribute is None:
      attribute = self.charAttr

    self.assertTrue(elementText.startswith('<ul'))
    self.assertTrue(elementText.endswith('</ul>'))
    self.assertElementAttributes(attribute, elementText, expectedAttributes)
    for item in items:
      self.assertIn('<li>%s</li>' % item, elementText)

  def testThatAttributeElementIsReturnedUsingAttributeReference(self):
    actual = createAttributeElement(self.context, self.charAttr)
    self.assertElementForSimpleAttribute(actual)

  def testThatAttributeElementIsReturnedUsingAttributeName(self):
    actual = createAttributeElement(self.context, self.charAttr.name)
    self.assertElementForSimpleAttribute(actual)

  def testThatAttributeElementIsReturnedUsingAttributeNameAsUnicode(self):
    actual = createAttributeElement(self.context, unicode(self.charAttr.name))
    self.assertElementForSimpleAttribute(actual)

  def testThatAttributeElementIsReturnedUsingAttributeNameWhenManyGameSystemsHaveSameAttributeName(self):
    gameSystem = GameSystem.objects.create(name = 'something else')
    CharacterAttribute.objects.create(gameSystem = gameSystem, name = self.charAttr.name)

    actual = createAttributeElement(self.context, self.charAttr.name)
    self.assertElementForSimpleAttribute(actual)

  def testThatDataInputAttributeIsSelectForConceptAttributes(self):
    attribute = self.addAttributeToCharacter(type = 'concept')
    actual = createAttributeElement(self.context, attribute.name)
    self.assertElementForSimpleAttribute(actual, expectedAttributes = {
      'data-editor': 'select'
    }, attribute = attribute)

  def testThatListElementIsReturnedForListAttributes(self):
    attribute = self.createAttribute(list = True)
    attr1 = self.createAttributeValueForCharacter(attribute, initialValue = self.uniqStr())
    attr2 = self.createAttributeValueForCharacter(attribute, initialValue = self.uniqStr())
    actual = createAttributeElement(self.context, attribute)
    self.assertElementForListAttribute(actual, [attr1.value, attr2.value], attribute = attribute)

