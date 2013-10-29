from teledu.models.lib import AttributeResolver
from teledu.models import ConceptInstance

class ConceptInstanceResolver(object):
  def __init__(self, concept):
    self.concept = concept

  def __unicode__(self):
    return unicode(self.concept.id)

  def __getattribute__(self, item):
    if item in ['concept', '_getConceptInstance']:
      return super(ConceptInstanceResolver, self).__getattribute__(item)
    instance = self._getConceptInstance(item)
    return AttributeResolver(instance)

  def _getConceptInstance(self, instanceName):
    return ConceptInstance.objects.get(concept = self.concept, name = instanceName)
