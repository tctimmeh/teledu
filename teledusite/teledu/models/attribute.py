from django.db import models
from teledu.models import DataType, Concept

class Attribute(models.Model):
  name = models.CharField(max_length = 30)
  dataType = models.ForeignKey(DataType, default = 1, verbose_name = 'Data Type')
  valueConcept = models.ForeignKey(Concept, null = True, blank = True)
  list = models.BooleanField(default = False)

  class Meta:
    abstract = True

  def isConcept(self):
    return self.dataType.isConcept()

  def getValue(self, instance):
    attributes = self.getAttributeValuesForInstance(instance)

    if not self.list:
      out = attributes[0].value
    else:
      out = []
      for attribute in attributes:
        out.append(attribute.value)
    return out

  def setValue(self, instance, newValue):
    self._deleteAttributeValues(instance)
    if isinstance(newValue, (list, tuple, set)):
      self._addAttributeValues(instance, newValue)
    else:
      self._addAttributeValue(instance, unicode(newValue))

  def setRawValue(self, instance, newValue):
    Attribute.setValue(self, instance, newValue)

  def _addAttributeValues(self, instance, rawValues):
    for rawValue in rawValues:
      self._addAttributeValue(instance, unicode(rawValue))

  def getAttributeValuesForInstance(self, instance):
    raise NotImplementedError()

  def _deleteAttributeValues(self, instance):
    raise NotImplementedError()

  def _addAttributeValue(self, instance, rawValue):
    raise NotImplementedError()

