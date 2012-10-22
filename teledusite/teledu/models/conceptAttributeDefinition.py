from django.db import models
from gameSystemConcept import  GameSystemConcept
from teledu.models.attributeDefinition import AttributeDefinition

class ConceptAttributeDefinition(AttributeDefinition):
  concept = models.ForeignKey(GameSystemConcept, related_name = 'attributeDefinitions')

  class Meta:
    app_label = 'teledu'
    unique_together = (('concept', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.valueConcept.name, self.name)

  def conceptName(self):
    return self.valueConcept.name

  def gameSystem(self):
    return self.valueConcept.gameSystem
