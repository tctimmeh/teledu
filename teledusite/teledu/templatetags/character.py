from django import template
from ..models import CharacterAttributeDefinition, DataType

register = template.Library()

def _createSpanAttributeElement(attributeDefinition, value):
  out = ['<span', 'id="attr_%d"' % attributeDefinition.id, 'class="char_attr"']
  if attributeDefinition.dataType.id == DataType.CONCEPT:
    out.append('data-editor="select"')
  out.append('>%s</span>' % value)
  return ' '.join(out)

def _createListAttributeElement(attributeDefinition, values):
  out = ['<ul', 'id="attr_%d"' % attributeDefinition.id, 'class="char_attr"', '>']
  for value in values:
    out.append('<li>%s</li>' % value)
  out.append('</ul>')
  return ' '.join(out)

@register.simple_tag(name = 'char_attr', takes_context = True)
def createAttributeElement(context, attributeDefinition):
  character = context['character']
  value = character.getAttributeValue(attributeDefinition)

  if isinstance(attributeDefinition, str) or isinstance(attributeDefinition, unicode):
    attributeDefinition = CharacterAttributeDefinition.objects.get(gameSystem = character.gameSystem, name = attributeDefinition)

  if attributeDefinition.list:
    return _createListAttributeElement(attributeDefinition, value)
  else:
    return _createSpanAttributeElement(attributeDefinition, value)

