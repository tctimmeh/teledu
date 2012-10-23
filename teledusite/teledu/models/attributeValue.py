from django.db import models

class AttributeValue(models.Model):
  raw_value = models.TextField(blank = True, default = '')

  class Meta:
    abstract = True

  @property
  def value(self):
    try:
      result = self.definition.dataType.translateValue(self.raw_value)
    except ValueError as e:
      raise ValueError('Failed to convert attribute [%s] with value [%s] to type [%s]: %s' % (
        self.definition, self.raw_value, self.definition.dataType.name, e))
    return result


