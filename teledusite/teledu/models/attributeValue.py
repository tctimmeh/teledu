from django.db import models

class AttributeValue(models.Model):
  raw_value = models.TextField(blank = True, default = '')

  class Meta:
    abstract = True

  @property
  def value(self):
    try:
      result = self.attribute.dataType.translateValue(self.raw_value)
    except ValueError as e:
      raise ValueError('Failed to convert attribute [%s] with value [%s] to type [%s]: %s' % (
        self.attribute, self.raw_value, self.attribute.dataType.name, e))
    return result


