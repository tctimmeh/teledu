from django import template
from ..models import CharacterAttributeDefinition

register = template.Library()

@register.simple_tag(takes_context = True)
def char_attr(context, attributeDefinition):
  character = context['character']

  if isinstance(attributeDefinition, str) or isinstance(attributeDefinition, unicode):
    attributeDefinition = CharacterAttributeDefinition.objects.get(gameSystem = character.gameSystem, name = attributeDefinition)

  attribute = character.getAttributeByDefinition(attributeDefinition)
  return '<span id="attr_%d" class="char_attr">%s</span>' % (
    attribute.id,
    attribute.value,
  )

