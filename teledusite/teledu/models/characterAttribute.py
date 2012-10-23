from django.db import models
from character import Character
from characterAttributeDefinition import CharacterAttributeDefinition
from lib import AttributeResolver
from attributeValue import AttributeValue

class CharacterAttribute(AttributeValue):
  character = models.ForeignKey(Character)
  definition = models.ForeignKey(CharacterAttributeDefinition)

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return '%s [%s] = [%s]' % (self.character.name, self.definition.name, self.raw_value)

  def calculateNewValue(self, **kwargs):
    if self.definition.calcFunction:
      newValue = self._execCalcFunction(kwargs)
      self.raw_value = newValue

    return self.raw_value

  def _execCalcFunction(self, scope):
    scope['attr'] = lambda name: AttributeResolver(self.character).getAttributeValue(name)
    scope['result'] = None
    exec self.definition.calcFunction in scope
    return scope['result']


