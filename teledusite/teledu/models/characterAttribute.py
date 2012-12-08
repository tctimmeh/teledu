from django.db import models
from gameSystem import GameSystem
from attribute import Attribute
from teledu.models.lib import AttributeDependentGraph
from teledu.models.lib import CalculationFunction

class CharacterAttribute(Attribute):
  gameSystem = models.ForeignKey(GameSystem, verbose_name = 'Game System', related_name = 'characterAttributes')
  default = models.CharField(max_length = 50, blank = True, default = '')
  calcFunction = models.TextField(null = True, blank = True, default = None, verbose_name = 'Calculation')
  display = models.BooleanField(default = True)

  class Meta:
    app_label = 'teledu'
    unique_together = (('gameSystem', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.gameSystem.name, self.name)

  def getAttributesForInstance(self, instance):
    from characterAttributeValue import CharacterAttributeValue
    return CharacterAttributeValue.objects.filter(character = instance, attribute = self)

  def setValue(self, instance, newValue):
    super(CharacterAttribute, self).setValue(instance, newValue)

    attrGraph = AttributeDependentGraph(self)
    changedAttributes = {self.id: self.getValue(instance)}

    for dependentAttribute in attrGraph.items():
      newValue = dependentAttribute.calculateNewValue(instance)
      changedAttributes[dependentAttribute.id] = newValue

    return changedAttributes

  def calculateNewValue(self, character):
    function = CalculationFunction(self.calcFunction, self, character)
    function.execute()
    return function.result
