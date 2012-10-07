from django.db import models
from gameSystem import GameSystem

class CharacterSheet(models.Model):
  gameSystem = models.ForeignKey(GameSystem, verbose_name = 'Game System')
  name = models.CharField(max_length = 50)
  template = models.TextField(blank = True, default = '')

  class Meta:
    app_label = 'teledu'
    unique_together = (('gameSystem', 'name'))

  def __unicode__(self):
    return self.name

