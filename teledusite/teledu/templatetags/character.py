from django import template
from ..models import CharacterAttributeDefinition, DataType

register = template.Library()

@register.simple_tag(takes_context = True)
def char_attr(context, attributeDefinition):
  character = context['character']

  if isinstance(attributeDefinition, str) or isinstance(attributeDefinition, unicode):
    attributeDefinition = CharacterAttributeDefinition.objects.get(gameSystem = character.gameSystem, name = attributeDefinition)

  value = character.getAttributeValue(attributeDefinition)
  out = ['<span', 'id="attr_%d"' % attributeDefinition.id, 'class="char_attr"']
  if attributeDefinition.dataType.id == DataType.CONCEPT:
    out.append('data-editor="select"')
  out.append('>%s</span>' % value)
  return ' '.join(out)

