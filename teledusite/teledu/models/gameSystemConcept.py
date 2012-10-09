from django.db import models
from teledu.models import GameSystem

class GameSystemConcept(models.Model):
  gameSystem = models.ForeignKey(GameSystem, verbose_name = 'Game System')
  name = models.CharField(max_length = 30)

  class Meta:
    app_label = 'teledu'
    unique_together = (('gameSystem', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.gameSystem.name, self.name)

