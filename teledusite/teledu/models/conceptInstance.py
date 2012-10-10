from django.db import models
from conceptAttributeDefinition import ConceptAttributeDefinition
from gameSystemConcept import GameSystemConcept

class ConceptInstance(models.Model):
  name = models.CharField(max_length = 50)
  concept = models.ForeignKey(GameSystemConcept)
  attributes = models.ManyToManyField(ConceptAttributeDefinition, through = 'ConceptInstanceAttribute')

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    if not len(self.attributes.all()):
      return 'Uninitialized concept instance - %s' % self.name
    return '%s - %s - %s' % (self.attributes.all()[0].concept.gameSystem.name, self.attributes.all()[0].concept.name, self.name)

