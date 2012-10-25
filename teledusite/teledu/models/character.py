from django.db import models
from .lib import AttributeDependentGraph
from characterAttribute import CharacterAttribute

class Character(models.Model):
  name = models.CharField(max_length = 50)
  attributes = models.ManyToManyField(CharacterAttribute, through = 'CharacterAttributeValue')

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

  def getAttributeValue(self, definition):
    definition = self._getAttributeDefinition(definition)
    return definition.getAttributeValue(self)

  def setAttributeValue(self, definition, value):
    definition = self._getAttributeDefinition(definition)
    return definition.setAttributeValue(self, value)

  def _getAttributeDefinition(self, attribute):
    if isinstance(attribute, CharacterAttribute):
      return attribute
    elif isinstance(attribute, int):
      return CharacterAttribute.objects.get(pk = attribute)
    elif isinstance(attribute, str) or (isinstance(attribute, unicode)):
      return self.attributes.filter(name = attribute).distinct()[0]

  def recalculateAllAttributes(self):
    attrGraph = AttributeDependentGraph(self.attributes.all())
    for dep in attrGraph.items():
      dep.calculateNewValue(self)

  def addMissingCharacterAttributeDefinitions(self, gameSystem = None):
    if gameSystem is None:
      gameSystem = self.gameSystem

    for attributeDefinition in gameSystem.characterAttributes.all():
      attributes = attributeDefinition.getAttributesForInstance(self)
      if not attributes:
        self._createCharacterAttributeFromDefinition(attributeDefinition)

  def _getInitialValueForForAttributeDefinition(self, definition):
    from teledu.models import ConceptInstance
    if not definition.default:
      return definition.default

    if definition.dataType.isConcept():
      try:
        return ConceptInstance.objects.get(name = definition.default, concept = definition.valueConcept).id
      except ConceptInstance.DoesNotExist:
        return ''
    else:
      return definition.default

  def _createCharacterAttributeFromDefinition(self, attributeDefinition):
    initialValue = self._getInitialValueForForAttributeDefinition(attributeDefinition)
    CharacterAttributeValue.objects.create(character = self, definition = attributeDefinition, raw_value = initialValue)

from characterAttributeValue import CharacterAttributeValue

