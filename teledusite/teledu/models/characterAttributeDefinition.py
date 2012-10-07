from django.db import models
from .gameSystem import GameSystem

class CharacterAttributeDefinition(models.Model):
  gameSystem = models.ForeignKey(GameSystem)
  name = models.CharField(max_length = 30)
  calcFunction = models.TextField(null = True, blank = True, default = None)

  class Meta:
    app_label = 'teledu'
    unique_together = (('gameSystem', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.gameSystem.name, self.name)

