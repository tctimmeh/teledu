from django.db import models
from gameSystem import GameSystem
from attributeDefinition import AttributeDefinition

class CharacterAttributeDefinition(AttributeDefinition):
  gameSystem = models.ForeignKey(GameSystem, verbose_name = 'Game System', related_name = 'characterAttributeDefinitions')
  default = models.CharField(max_length = 50, blank = True, default = '')
  calcFunction = models.TextField(null = True, blank = True, default = None, verbose_name = 'Calculation')
  display = models.BooleanField(default = True)

  class Meta:
    app_label = 'teledu'
    unique_together = (('gameSystem', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.gameSystem.name, self.name)

  def _getAttributes(self, instance):
    from characterAttribute import CharacterAttribute
    return CharacterAttribute.objects.filter(character = instance, definition = self)

