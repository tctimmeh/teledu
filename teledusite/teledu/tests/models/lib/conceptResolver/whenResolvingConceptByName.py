from teledu.models.lib.conceptResolver import ConceptResolver
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenResolvingConceptByName(TeleduTestCase):
  def testReturnsConceptInstanceResolverForValidName(self):
    conceptResolver = ConceptResolver(self.gameSystem)
    actual = getattr(conceptResolver, self.concept.name)
    self.assertEqual(actual.concept.id, self.concept.id)
