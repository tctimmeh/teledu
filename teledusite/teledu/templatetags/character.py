from django import template

register = template.Library()

@register.filter(name = 'charAttr')
def charAttr(character, attribute):
  return character.getAttribute(attribute)
