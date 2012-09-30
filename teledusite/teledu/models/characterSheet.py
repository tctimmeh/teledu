from django.db import models
from gameSystem import GameSystem

class CharacterSheet(models.Model):
  gameSystem = models.ForeignKey(GameSystem)
  name = models.CharField(max_length = 50)
  template = models.TextField()

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return self.name

