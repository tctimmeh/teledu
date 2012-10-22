from django.db import models
from gameSystem import GameSystem
from gameSystemConcept import GameSystemConcept
from teledu.models.attributeDefinition import AttributeDefinition

class CharacterAttributeDefinition(AttributeDefinition):
  gameSystem = models.ForeignKey(GameSystem, verbose_name = 'Game System', related_name = 'characterAttributeDefinitions')
  concept = models.ForeignKey(GameSystemConcept, null = True, blank = True)
  default = models.CharField(max_length = 50, blank = True, default = '')
  calcFunction = models.TextField(null = True, blank = True, default = None, verbose_name = 'Calculation')
  list = models.BooleanField(default = False)
  display = models.BooleanField(default = True)

  class Meta:
    app_label = 'teledu'
    unique_together = (('gameSystem', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.gameSystem.name, self.name)

