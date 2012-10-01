import json
from django.db import models

from .character import Character
from .characterAttributeDefinition import CharacterAttributeDefinition

class CharacterAttribute(models.Model):
  character = models.ForeignKey(Character)
  attribute = models.ForeignKey(CharacterAttributeDefinition)
  value = models.TextField(null = True, blank = True, default = None)

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return '%s [%s] = [%s]' % (self.character.name, self.attribute.name, self.value)

  def asDict(self):
   return {
      'id': self.attribute.id,
      'name': self.attribute.name,
      'value': self.value,
    }

  def serialize(self):
    return json.dumps(self.asDict())

