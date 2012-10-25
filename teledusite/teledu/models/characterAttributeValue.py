from django.db import models
from character import Character
from characterAttribute import CharacterAttribute
from attributeValue import AttributeValue

class CharacterAttributeValue(AttributeValue):
  character = models.ForeignKey(Character)
  definition = models.ForeignKey(CharacterAttribute)

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return '%s [%s] = [%s]' % (self.character.name, self.definition.name, self.raw_value)

