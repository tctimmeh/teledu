from teledu.models import Concept
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingConceptByName(TeleduTestCase):
  def testConceptObjectIsReturnedForValidName(self):
    actual = Concept.getConcept(self.gameSystem, self.concept.name)
    self.assertEqual(actual.id, self.concept.id)
