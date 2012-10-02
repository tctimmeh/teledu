from django import template
from ..models import CharacterAttributeDefinition

register = template.Library()

@register.simple_tag(takes_context = True)
def char_attr(context, attribute):
  character = context['character']

  if isinstance(attribute, str) or isinstance(attribute, unicode):
    attribute = CharacterAttributeDefinition.objects.get(gameSystem = character.gameSystem, name = attribute)

  return '<span id="attr_%d">%s</span>' % (
    attribute.id,
    character.getAttribute(attribute),
  )

