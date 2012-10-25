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

