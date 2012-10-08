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

  @property
  def gameSystem(self):
    return self.attributes.all()[0].gameSystem

  def attributesByName(self):
    return self.attributes.all().order_by('name')

  @classmethod
  def create(cls, gameSystem, name):
    newCharacter = Character.objects.create(name = name)
    for attribute in CharacterAttributeDefinition.objects.filter(gameSystem = gameSystem):
      CharacterAttribute.objects.create(character = newCharacter, definition = attribute, raw_value = attribute.default)
    return newCharacter

  def serialize(self):
    attributes = CharacterAttribute.objects.filter(character = self)
    return json.dumps({
      'id': self.id,
      'name': self.name,
      'attributes': [attribute.asDict() for attribute in attributes],
    })

  def getAttributeValueByName(self, attributeName):
    return CharacterAttribute.objects.get(character = self, definition__name = attributeName).value

  def getAttributeValueByDefinition(self, attributeDefinition):
    if isinstance(attributeDefinition, int):
      attributeDefinition = CharacterAttributeDefinition.objects.get(pk = attributeDefinition)

    attribute = CharacterAttribute.objects.get(character = self, definition = attributeDefinition)
    return attribute.value

  def setAttributeValue(self, attrDefinition, value):
    attrGraph = AttributeDependentGraph(attrDefinition)

    self._setAttr(attrDefinition, value)
    for dep in attrGraph.items():
      self._calculateAttributeValue(dep)

  def _setAttr(self, attrDef, value):
    attribute = CharacterAttribute.objects.get(character = self, definition = attrDef)
    attribute.raw_value = value
    attribute.save()

  def _calculateAttributeValue(self, attrDefn):
    attribute = CharacterAttribute.objects.get(character = self, definition = attrDefn)
    attribute.calculateNewValue(char = self)
    attribute.save()

from characterAttribute import CharacterAttribute

