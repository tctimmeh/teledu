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
    from teledu.models import ConceptInstance

    newCharacter = Character.objects.create(name = name)
    for attributeDefinition in CharacterAttributeDefinition.objects.filter(gameSystem = gameSystem):
      if attributeDefinition.dataType.isConcept():
        try:
          initialValue = ConceptInstance.objects.get(name = attributeDefinition.default, concept = attributeDefinition.concept).id
        except ObjectDoesNotExist, e:
          initialValue = ''
      else:
        initialValue = attributeDefinition.default

      CharacterAttribute.objects.create(character = newCharacter, definition = attributeDefinition, raw_value = initialValue)
    return newCharacter

  def serialize(self):
    attributes = CharacterAttribute.objects.filter(character = self)
    return json.dumps({
#      'id': self.id,
#      'name': self.name,
#      'attributes': [attribute.asDict() for attribute in attributes],
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
    changedAttributes = {attrDefinition.id: value}

    for dep in attrGraph.items():
      newValue = self._calculateAttributeValue(dep)
      changedAttributes[dep.id] = newValue

    return changedAttributes

  def recalculateAllAttributes(self):
    attrGraph = AttributeDependentGraph(self.attributes.all())
    for dep in attrGraph.items():
      self._calculateAttributeValue(dep)

  def _setAttr(self, attrDef, value):
    attribute = CharacterAttribute.objects.get(character = self, definition = attrDef)
    attribute.raw_value = value
    attribute.save()

  def _calculateAttributeValue(self, attrDefn):
    attribute = CharacterAttribute.objects.get(character = self, definition = attrDefn)
    attribute.calculateNewValue()
    attribute.save()
    return attribute.raw_value

  def addMissingCharacterAttributeDefinitions(self):
    attributeDefinitions = self._retreiveAllEligibleCharacterAttributeDefinitionsForThisCharacter()
    for attributeDefinition in attributeDefinitions:
      try:
        self._retreiveCharacterAttributeForCharacterAttributeDefinition(attributeDefinition)
      except ObjectDoesNotExist, e:
        self._createCharacterAttributeFromCharacterAttributeDefinition(attributeDefinition)
        self.save()

  def _retreiveAllEligibleCharacterAttributeDefinitionsForThisCharacter(self):
    return CharacterAttributeDefinition.objects.filter(gameSystem = self.gameSystem)

  def _retreiveCharacterAttributeForCharacterAttributeDefinition(self, attributeDefinition):
    return CharacterAttribute.objects.get(character = self, definition = attributeDefinition)

  def _createCharacterAttributeFromCharacterAttributeDefinition(self, attributeDefinition):
    from teledu.models import ConceptInstance
    if attributeDefinition.dataType.isConcept():
      try:
        initialValue = ConceptInstance.objects.get(name = attributeDefinition.default, concept = attributeDefinition.concept).id
      except ObjectDoesNotExist, e:
        initialValue = ''
    else:
      initialValue = attributeDefinition.default
    CharacterAttribute.objects.create(character = self, definition = attributeDefinition, raw_value = initialValue)

from characterAttribute import CharacterAttribute

