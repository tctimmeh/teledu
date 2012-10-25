from django.db import models
from gameSystem import GameSystem
from attribute import Attribute
from teledu.models.lib import AttributeDependentGraph, AttributeResolver

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

  def setAttributeValue(self, instance, newValue):
    super(CharacterAttribute, self).setAttributeValue(instance, newValue)

    attrGraph = AttributeDependentGraph(self)
    changedAttributes = {self.id: self.getAttributeValue(instance)}

    for dependentAttribute in attrGraph.items():
      newValue = dependentAttribute.calculateNewValue(instance)
      changedAttributes[dependentAttribute.id] = newValue

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



