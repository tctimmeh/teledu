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

  def setValue(self, instance, newValue):
    super(CharacterAttribute, self).setValue(instance, newValue)

    attrGraph = AttributeDependentGraph(self)
    changedAttributes = {self.id: self.getValue(instance)}

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
      'character': AttributeResolver2(character),
      'result': None
    }
    exec self.calcFunction in scope
    return scope['result']


class AttributeResolver2(object):
  def __init__(self, modelObject):
    self.modelObject = modelObject

  def __getattribute__(self, item):
    from teledu.models import CharacterAttributeValue
    if item in ['modelObject']:
      return super(AttributeResolver2, self).__getattribute__(item)
    attribute = self.modelObject.getAttribute(item)
    if attribute.isConcept():
      attributeValue = CharacterAttributeValue.objects.get(attribute = attribute, character = self.modelObject)
      return attributeValue.raw_value
    return attribute.getValue(self.modelObject)

