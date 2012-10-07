import json
from django.db import models

from .character import Character
from .characterAttributeDefinition import CharacterAttributeDefinition

class CharacterAttribute(models.Model):
  character = models.ForeignKey(Character)
  definition = models.ForeignKey(CharacterAttributeDefinition)
  value = models.TextField(blank = True, default = '')

  class Meta:
    app_label = 'teledu'
    unique_together = (('character', 'definition'))

  def __unicode__(self):
    return '%s [%s] = [%s]' % (self.character.name, self.definition.name, self.value)

  def asDict(self):
   return {
      'id': self.definition.id,
      'name': self.definition.name,
      'value': self.value,
    }

  def serialize(self):
    return json.dumps(self.asDict())

  def calculateNewValue(self, char, **kwargs):
    newValue = self._execCalcFunction(char, kwargs)
    self.value = newValue

  def _execCalcFunction(self, char, scope):
    scope['attr'] = lambda name: char.attr(name)
    scope['result'] = None
    exec self.definition.calcFunction in scope
    return scope['result']


