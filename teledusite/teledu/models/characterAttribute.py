import json
from django.db import models

from .character import Character
from .characterAttributeDefinition import CharacterAttributeDefinition

class CharacterAttribute(models.Model):
  character = models.ForeignKey(Character)
  definition = models.ForeignKey(CharacterAttributeDefinition)
  value = models.TextField(null = True, blank = True, default = None)

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

