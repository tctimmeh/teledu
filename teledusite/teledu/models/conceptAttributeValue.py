from django.db import models
from conceptAttribute import ConceptAttribute
from conceptInstance import ConceptInstance
from teledu.models.attributeValue import AttributeValue

class ConceptAttributeValue(AttributeValue):
  definition = models.ForeignKey(ConceptAttribute)
  instance = models.ForeignKey(ConceptInstance)

  class Meta:
    app_label = 'teledu'
    unique_together = (('definition', 'instance'))

  def __unicode__(self):
    return '%s [%s] = [%s]' % (self.instance.name, self.definition.name, self.raw_value)

