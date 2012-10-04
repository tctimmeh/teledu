import json
from django.db import models
from characterAttributeDefinition import CharacterAttributeDefinition

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
    attrSets = self._getLayeredDependentsForAttribute(attrDefinition)
    attrSets = self._cullDuplicatesFromDependencyLayers(attrSets)

    self._setAttr(attrDefinition, value)
    for depSet in attrSets:
      for dep in depSet:
        self._calculateAttributeValue(dep)

  def _setAttr(self, attrDef, value):
    attribute = CharacterAttribute.objects.get(character = self, definition = attrDef)
    attribute.value = value
    attribute.save()

  def _calculateAttributeValue(self, attrDefn):
    attribute = CharacterAttribute.objects.get(character = self, definition = attrDefn)
    attribute.calculateNewValue(char = self)
    attribute.save()

  def _getLayeredDependentsForAttribute(self, defn):
    attrSets = []

    deps = set(defn.dependents.all())
    depList = []
    for dep in deps:
      depList.append(dep.attribute)
    attrSets.append(depList)

    while depList:
      depSet = set()
      for dep in depList:
        newDeps = set(dep.dependents.all())
        depSet = depSet.union(newDeps)
      depList = []
      for dep in depSet:
        depList.append(dep.attribute)
      attrSets.append(depList)

    return attrSets

  def _cullDuplicatesFromDependencyLayers(self, attrSets):
    finalAttrs = []
    allDeps = set()
    for deps in reversed(attrSets):
      finalDeps = set()
      for dep in deps:
        if dep not in allDeps:
          finalDeps.add(dep)
          allDeps.add(dep)
      if finalDeps:
        finalAttrs.insert(0, finalDeps)
    return finalAttrs

from characterAttribute import CharacterAttribute

