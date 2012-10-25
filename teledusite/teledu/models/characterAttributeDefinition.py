from django.db import models
from gameSystem import GameSystem
from attributeDefinition import AttributeDefinition
from teledu.models.lib import AttributeDependentGraph, AttributeResolver

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

  def getAttributesForInstance(self, instance):
    from characterAttribute import CharacterAttribute
    return CharacterAttribute.objects.filter(character = instance, definition = self)

  def setAttributeValue(self, instance, newValue):
    super(CharacterAttributeDefinition, self).setAttributeValue(instance, newValue)

    attrGraph = AttributeDependentGraph(self)
    changedAttributes = {self.id: self.getAttributeValue(instance)}

    for dependentDefinition in attrGraph.items():
      newValue = dependentDefinition.calculateNewValue(instance)
      changedAttributes[dependentDefinition.id] = newValue

    return changedAttributes

  def calculateNewValue(self, character):
    attributeValue = self.getAttributesForInstance(character)[0]
    if self.calcFunction:
      newValue = self._execCalcFunction(character)
      attributeValue.raw_value = newValue
      attributeValue.save()

    return attributeValue.value

  def _execCalcFunction(self, character):
    scope = {
      'attr': lambda name: AttributeResolver(character).getAttributeValue(name),
      'result': None
    }
    exec self.calcFunction in scope
    return scope['result']



