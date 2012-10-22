from django.db import models
from conceptAttributeDefinition import ConceptAttributeDefinition
from conceptInstance import ConceptInstance
from teledu.models.attributeValue import AttributeValue

class ConceptInstanceAttribute(AttributeValue):
  definition = models.ForeignKey(ConceptAttributeDefinition)
  instance = models.ForeignKey(ConceptInstance)

  class Meta:
    app_label = 'teledu'
    unique_together = (('definition', 'instance'))

  def __unicode__(self):
    return '%s [%s] = [%s]' % (self.instance.name, self.definition.name, self.raw_value)

