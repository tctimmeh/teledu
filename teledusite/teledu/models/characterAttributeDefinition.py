from django.db import models
from gameSystem import GameSystem
from dataType import DataType
from gameSystemConcept import GameSystemConcept

class CharacterAttributeDefinition(models.Model):
  gameSystem = models.ForeignKey(GameSystem, verbose_name = 'Game System')
  name = models.CharField(max_length = 30)
  dataType = models.ForeignKey(DataType, verbose_name = 'Data Type', default = 1)
  concept = models.ForeignKey(GameSystemConcept, null = True, blank = True)
  default = models.CharField(max_length = 50, blank = True, default = '')
  calcFunction = models.TextField(null = True, blank = True, default = None, verbose_name = 'Calculation')

  class Meta:
    app_label = 'teledu'
    unique_together = (('gameSystem', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.gameSystem.name, self.name)

