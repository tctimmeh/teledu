from django.db import models
from conceptAttribute import ConceptAttribute
from conceptInstance import ConceptInstance
from teledu.models.attributeValue import AttributeValue

class ConceptAttributeValue(AttributeValue):
  attribute = models.ForeignKey(ConceptAttribute)
  instance = models.ForeignKey(ConceptInstance)

  class Meta:
    app_label = 'teledu'
    unique_together = (('attribute', 'instance'))

  def __unicode__(self):
    return '%s [%s] = [%s]' % (self.instance.name, self.attribute.name, self.raw_value)

