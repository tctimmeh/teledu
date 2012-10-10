from django.db import models

class DataType(models.Model):
  name = models.CharField(max_length = 15, unique = True)

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return self.name

  def translateValue(self, value):
    from teledu.models import ConceptInstance
    # These magic numbers must match those found in the initial_data.json fixture
    if self.id == 4:
      return ConceptInstance.objects.get(pk = int(value)).name
    elif self.id == 3:
      return float(value)
    elif self.id == 2:
      return int(value)
    return value

  def isConcept(self):
    return self.id == 4

