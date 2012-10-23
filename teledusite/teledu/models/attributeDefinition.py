from django.db import models
from teledu.models import DataType, GameSystemConcept

class AttributeDefinition(models.Model):
  name = models.CharField(max_length = 30)
  dataType = models.ForeignKey(DataType, default = 1, verbose_name = 'Data Type')
  valueConcept = models.ForeignKey(GameSystemConcept, null = True, blank = True)
  list = models.BooleanField(default = False)

  class Meta:
    abstract = True

  def getAttributeValue(self, instance):
    attributes = self.getAttributesForInstance(instance)

    if not self.list:
      out = attributes[0].value
    else:
      out = []
      for attribute in attributes:
        out.append(attribute.value)
    return out

  def setAttributeValue(self, instance, newValue):
    attribute = self.getAttributesForInstance(instance)[0]
    attribute.raw_value = newValue
    attribute.save()

  def getAttributesForInstance(self, instance):
    raise NotImplementedError()

