from django.db import models

class DataType(models.Model):
  name = models.CharField(max_length = 15, unique = True)

  # These magic numbers must match those found in the initial_data.json fixture
  TEXT = 1
  INTEGER = 2
  REAL = 3
  CONCEPT = 4

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return self.name

  def translateValue(self, value):
    from teledu.models import ConceptInstance
    if self.id == DataType.CONCEPT:
      if not value:
        return ''
      return ConceptInstance.objects.get(pk = int(value)).name
    elif self.id == DataType.REAL:
      return float(value)
    elif self.id == DataType.INTEGER:
      return int(value)
    return value

  def isConcept(self):
    return self.id == DataType.CONCEPT

  def isText(self):
    return self.id == DataType.TEXT

