from teledu.models.lib.conceptInstanceResolver import ConceptInstanceResolver
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenResolvingConceptInstance(TeleduTestCase):
  def testAttributeResolverForInstanceIsReturned(self):
    conceptInstance = self.createConceptInstance()
    resolver = ConceptInstanceResolver(self.concept)
    actual = getattr(resolver, conceptInstance.name)
    self.assertEqual(actual.modelObject.id, conceptInstance.id)

