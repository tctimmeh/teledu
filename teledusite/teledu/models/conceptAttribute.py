from django.db import models
from concept import Concept
from attribute import Attribute

class ConceptAttribute(Attribute):
  concept = models.ForeignKey(Concept, related_name = 'attributes')

  class Meta:
    app_label = 'teledu'
    unique_together = (('concept', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.concept.name, self.name)

  def conceptName(self):
    return self.concept.name

  def gameSystem(self):
    return self.concept.gameSystem

  def getAttributesForInstance(self, instance):
    from conceptAttributeValue import ConceptAttributeValue
    return ConceptAttributeValue.objects.filter(attribute = self, instance = instance)

