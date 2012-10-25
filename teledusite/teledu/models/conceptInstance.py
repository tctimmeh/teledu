from django.db import models
from conceptAttribute import ConceptAttribute
from django.db.models.signals import post_save
from django.dispatch import receiver
from concept import Concept

class ConceptInstance(models.Model):
  name = models.CharField(max_length = 50)
  concept = models.ForeignKey(Concept)
  attributes = models.ManyToManyField(ConceptAttribute, through = 'ConceptAttributeValue')

  class Meta:
    app_label = 'teledu'
    unique_together = (('concept', 'name'))

  def __unicode__(self):
    return '%s - %s - %s' % (self.concept.gameSystem.name, self.concept.name, self.name)

  def gameSystem(self):
    return self.concept.gameSystem

  def conceptName(self):
    return self.concept.name

@receiver(post_save, sender = ConceptInstance, dispatch_uid = 'concept_instance_post_save')
def createConceptInstanceAttributes(sender, **kwargs):
  instance = kwargs['instance']
  created = kwargs['created']
  raw = kwargs['raw']

  if raw or not created:
    return

  from conceptAttributeValue import ConceptAttributeValue
  definitions = instance.concept.attributeDefinitions.all()
  for definition in definitions:
    ConceptAttributeValue.objects.create(instance = instance, definition = definition)

