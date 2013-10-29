from django.db import models
from gameSystem import GameSystem

class Concept(models.Model):
  gameSystem = models.ForeignKey(GameSystem, verbose_name = 'Game System')
  name = models.CharField(max_length = 30)

  class Meta:
    app_label = 'teledu'
    unique_together = (('gameSystem', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.gameSystem.name, self.name)

  @classmethod
  def getConcept(cls, gameSystem, conceptName):
    return cls.objects.get(gameSystem = gameSystem, name = conceptName)
