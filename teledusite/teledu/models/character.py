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
    newCharacter.addMissingCharacterAttributes(gameSystem = gameSystem)
    return newCharacter

  def getAttributeValue(self, attribute):
    attribute = self._getAttribute(attribute)
    return attribute.getValue(self)

  def setAttributeValue(self, attribute, value):
    attribute = self._getAttribute(attribute)
    return attribute.setValue(self, value)

  def _getAttribute(self, attribute):
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

  def addMissingCharacterAttributes(self, gameSystem = None):
    if gameSystem is None:
      gameSystem = self.gameSystem

    for attribute in gameSystem.characterAttributes.all():
      attributes = attribute.getAttributesForInstance(self)
      if not attributes:
        self._createAttributeValue(attribute)

  def _getInitialValueForForAttribute(self, attribute):
    from teledu.models import ConceptInstance
    if not attribute.default:
      return attribute.default

    if attribute.dataType.isConcept():
      try:
        return ConceptInstance.objects.get(name = attribute.default, concept = attribute.valueConcept).id
      except ConceptInstance.DoesNotExist:
        return ''
    else:
      return attribute.default

  def _createAttributeValue(self, attribute):
    initialValue = self._getInitialValueForForAttribute(attribute)
    CharacterAttributeValue.objects.create(character = self, attribute = attribute, raw_value = initialValue)

from characterAttributeValue import CharacterAttributeValue

