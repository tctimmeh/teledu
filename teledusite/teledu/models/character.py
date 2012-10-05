import json
from django.db import models
from characterAttributeDefinition import CharacterAttributeDefinition
from .lib import AttributeDependentGraph

class Character(models.Model):
  name = models.CharField(max_length = 50)
  attributes = models.ManyToManyField(CharacterAttributeDefinition, through = 'CharacterAttribute')

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return self.name

  def serialize(self):
    attributes = CharacterAttribute.objects.filter(character = self)
    return json.dumps({
      'id': self.id,
      'name': self.name,
      'attributes': [attribute.asDict() for attribute in attributes],
    })

  @property
  def gameSystem(self):
    return self.attributes.all()[0].gameSystem

  def attr(self, attributeName):
    return CharacterAttribute.objects.get(character = self, definition__name = attributeName).value

  def getAttributeByDefinition(self, attributeDefinition):
    return CharacterAttribute.objects.get(character = self, definition = attributeDefinition)

  def getAttributeValueByDefinition(self, attributeDefinition):
    return self.getAttributeByDefinition(attributeDefinition).value

  def setAttributeValue(self, attrDefinition, value):
    attrGraph = AttributeDependentGraph(attrDefinition)

    self._setAttr(attrDefinition, value)
    for dep in attrGraph.items():
      self._calculateAttributeValue(dep)

  def _setAttr(self, attrDef, value):
    attribute = CharacterAttribute.objects.get(character = self, definition = attrDef)
    attribute.value = value
    attribute.save()

  def _calculateAttributeValue(self, attrDefn):
    attribute = CharacterAttribute.objects.get(character = self, definition = attrDefn)
    attribute.calculateNewValue(char = self)
    attribute.save()

from characterAttribute import CharacterAttribute

