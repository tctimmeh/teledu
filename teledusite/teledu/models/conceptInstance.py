from django.db import models
from teledu.models import ConceptAttributeDefinition

class ConceptInstance(models.Model):
  name = models.CharField(max_length = 50)
  attributes = models.ManyToManyField(ConceptAttributeDefinition, through = 'ConceptInstanceAttribute')

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return '%s - %s - %s' % (self.attributes.all()[0].concept.gameSystem.name, self.attributes.all()[0].concept.name, self.name)

