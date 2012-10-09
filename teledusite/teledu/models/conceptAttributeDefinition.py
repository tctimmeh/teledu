from django.db import models
from teledu.models import  GameSystemConcept, DataType

class ConceptAttributeDefinition(models.Model):
  concept = models.ForeignKey(GameSystemConcept)
  name = models.CharField(max_length = 30)
  dataType = models.ForeignKey(DataType, default = 1, verbose_name = 'Data Type')

  class Meta:
    app_label = 'teledu'
    unique_together = (('concept', 'name'))

  def __unicode__(self):
    return '%s - %s' % (self.concept.name, self.name)

