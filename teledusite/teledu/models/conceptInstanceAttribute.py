from django.db import models
from teledu.models import ConceptAttributeDefinition, ConceptInstance

class ConceptInstanceAttribute(models.Model):
  definition = models.ForeignKey(ConceptAttributeDefinition)
  instance = models.ForeignKey(ConceptInstance)
  raw_value = models.TextField(blank = True, default = '')

  class Meta:
    app_label = 'teledu'
    unique_together = (('definition', 'instance'))

  def __unicode__(self):
    return '%s [%s] = %s' % (self.instance.name, self.definition.name, self.raw_value)

