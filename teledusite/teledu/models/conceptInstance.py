from django.db import models
from conceptAttributeDefinition import ConceptAttributeDefinition
from django.db.models.signals import post_save
from django.dispatch import receiver
from gameSystemConcept import GameSystemConcept

class ConceptInstance(models.Model):
  name = models.CharField(max_length = 50)
  concept = models.ForeignKey(GameSystemConcept)
  attributes = models.ManyToManyField(ConceptAttributeDefinition, through = 'ConceptInstanceAttribute')

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

  from conceptInstanceAttribute import ConceptInstanceAttribute
  definitions = instance.concept.attributeDefinitions.all()
  for definition in definitions:
    ConceptInstanceAttribute.objects.create(instance = instance, definition = definition)

