from teledu.models import Concept
from teledu.models.lib.conceptInstanceResolver import ConceptInstanceResolver

class ConceptResolver(object):
  def __init__(self, gameSystem):
    self.gameSystem = gameSystem

  def __unicode__(self):
    return unicode(self.gameSystem.id)

  def __getattribute__(self, item):
    if item in ['gameSystem', '_getConcept']:
      return super(ConceptResolver, self).__getattribute__(item)
    concept = self._getConcept(item)
    return ConceptInstanceResolver(concept)

  def _getConcept(self, conceptName):
    return Concept.getConcept(self.gameSystem, conceptName)

