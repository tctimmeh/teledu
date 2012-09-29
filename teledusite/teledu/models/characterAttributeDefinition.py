from django.db import models
from .gameSystem import GameSystem

class CharacterAttributeDefinition(models.Model):
  gameSystem = models.ForeignKey(GameSystem)
  name = models.CharField(max_length = 30)

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return self.name

