from django.template import Context
from teledu.tests.teleduTestCase import TeleduTestCase
from teledu.models import GameSystem, CharacterAttributeDefinition
from teledu.templatetags.character import char_attr

class WhenEmbeddingCharacterAttribute(TeleduTestCase):
  def setUp(self):
    super(WhenEmbeddingCharacterAttribute, self).setUp()
    self.context = Context()
    self.context['character'] = self.character

  def assertCorrectAttributeElement(self, elementText):
    self.assertEqual(elementText, '<span id="attr_%d" class="char_attr">%s</span>' % (self.charAttrDefn.id, self.charAttrValue))

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


