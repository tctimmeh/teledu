from django.db import models
from .characterAttributeDefinition import CharacterAttributeDefinition

class Character(models.Model):
  name = models.CharField(max_length = 50)
  attributes = models.ManyToManyField(CharacterAttributeDefinition, through = 'CharacterAttribute')

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return self.name

  def getAttribute(self, id):
    return CharacterAttribute.objects.get(character = self, attribute = id).value

from .characterAttribute import CharacterAttribute

