from django import template
from ..models import CharacterAttribute, DataType

register = template.Library()

def _createSpanAttributeElement(attribute, value):
  out = ['<span', 'id="attr_%d"' % attribute.id, 'class="char_attr"']
  if attribute.dataType.id == DataType.CONCEPT:
    out.append('data-editor="select"')
  out.append('>%s</span>' % value)
  return ' '.join(out)

def _createListAttributeElement(attribute, values):
  out = ['<ul', 'id="attr_%d"' % attribute.id, 'class="char_attr"', '>']
  for value in values:
    out.append('<li>%s</li>' % value)
  out.append('</ul>')
  return ' '.join(out)

@register.simple_tag(name = 'char_attr', takes_context = True)
def createAttributeElement(context, attribute):
  character = context['character']
  value = character.getAttributeValue(attribute)

  if isinstance(attribute, str) or isinstance(attribute, unicode):
    attribute = CharacterAttribute.objects.get(gameSystem = character.gameSystem, name = attribute)

  if attribute.list:
    return _createListAttributeElement(attribute, value)
  else:
    return _createSpanAttributeElement(attribute, value)

