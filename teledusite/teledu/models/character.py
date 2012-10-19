import json
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from .lib import AttributeDependentGraph
from characterAttributeDefinition import CharacterAttributeDefinition

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
    newCharacter.addMissingCharacterAttributeDefinitions(gameSystem = gameSystem)
    return newCharacter

  def getAttributeValue(self, attribute):
    if isinstance(attribute, str) or (isinstance(attribute, unicode)):
      attribute = self.getAttributeByName(attribute)
    elif isinstance(attribute, int) or isinstance(attribute, CharacterAttributeDefinition):
      attribute = self.getAttributeByDefinition(attribute)

    return attribute.value

  def getAttributeByDefinition(self, attributeDefinition):
    return CharacterAttribute.objects.get(character = self, definition = attributeDefinition)

  def getAttributeByName(self, name):
    return CharacterAttribute.objects.get(character = self, definition__name = name)

  def setAttributeValue(self, attrDefinition, value):
    attrGraph = AttributeDependentGraph(attrDefinition)

    self._setAttr(attrDefinition, value)
    changedAttributes = {attrDefinition.id: self.getAttributeValue(attrDefinition)}

    for dep in attrGraph.items():
      newValue = self._calculateAttributeValue(dep)
      changedAttributes[dep.id] = newValue

    return changedAttributes

  def recalculateAllAttributes(self):
    attrGraph = AttributeDependentGraph(self.attributes.all())
    for dep in attrGraph.items():
      self._calculateAttributeValue(dep)

  def _setAttr(self, attrDef, value):
    attribute = self.getAttributeByDefinition(attrDef)
    attribute.raw_value = value
    attribute.save()

  def _calculateAttributeValue(self, attrDefn):
    attribute = self.getAttributeByDefinition(attrDefn)
    attribute.calculateNewValue()
    attribute.save()
    return attribute.value

  def addMissingCharacterAttributeDefinitions(self, gameSystem = None):
    if gameSystem is None:
      gameSystem = self.gameSystem

    for attributeDefinition in gameSystem.characterAttributeDefinitions.all():
      try:
        self.getAttributeByDefinition(attributeDefinition)
      except ObjectDoesNotExist, e:
        self._createCharacterAttributeFromDefinition(attributeDefinition)

  def _getInitialValueForForAttributeDefinition(self, definition):
    from teledu.models import ConceptInstance

    if definition.dataType.isConcept():
      try:
        return ConceptInstance.objects.get(name = definition.default, concept = definition.concept).id
      except ObjectDoesNotExist, e:
        return ''
    else:
      return definition.default

  def _createCharacterAttributeFromDefinition(self, attributeDefinition):
    initialValue = self._getInitialValueForForAttributeDefinition(attributeDefinition)
    CharacterAttribute.objects.create(character = self, definition = attributeDefinition, raw_value = initialValue)

from characterAttribute import CharacterAttribute

