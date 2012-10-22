from django.db import models
from teledu.models import DataType, GameSystemConcept

class AttributeDefinition(models.Model):
  name = models.CharField(max_length = 30)
  dataType = models.ForeignKey(DataType, default = 1, verbose_name = 'Data Type')
  valueConcept = models.ForeignKey(GameSystemConcept, null = True, blank = True)
  list = models.BooleanField(default = False)

  class Meta:
    abstract = True

