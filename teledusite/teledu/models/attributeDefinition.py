from django.db import models
from teledu.models import DataType

class AttributeDefinition(models.Model):
  name = models.CharField(max_length = 30)
  dataType = models.ForeignKey(DataType, default = 1, verbose_name = 'Data Type')

  class Meta:
    abstract = True

