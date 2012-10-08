import json
from django.db import models

from .character import Character
from .characterAttributeDefinition import CharacterAttributeDefinition

class CharacterAttribute(models.Model):
  character = models.ForeignKey(Character)
  definition = models.ForeignKey(CharacterAttributeDefinition)
  raw_value = models.TextField(blank = True, default = '')

  class Meta:
    app_label = 'teledu'
    unique_together = (('character', 'definition'))

  def __unicode__(self):
    return '%s [%s] = [%s]' % (self.character.name, self.definition.name, self.raw_value)

  @property
  def value(self):
    try:
      result = self.definition.dataType.translateValue(self.raw_value)
    except ValueError, e:
      raise ValueError('Failed to convert attribute [%s] with value [%s] to type [%s]' % (
        self.definition, self.raw_value, self.definition.dataType.name))
    return result

  def asDict(self):
   return {
      'id': self.definition.id,
      'name': self.definition.name,
      'value': self.raw_value,
    }

  def serialize(self):
    return json.dumps(self.asDict())

  def calculateNewValue(self, char, **kwargs):
    newValue = self._execCalcFunction(char, kwargs)
    self.raw_value = newValue

  def _execCalcFunction(self, char, scope):
    scope['attr'] = lambda name: char.getAttributeValueByName(name)
    scope['result'] = None
    exec self.definition.calcFunction in scope
    return scope['result']


