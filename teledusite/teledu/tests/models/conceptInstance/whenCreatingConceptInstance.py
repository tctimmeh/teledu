from teledu.models import ConceptInstance, ConceptAttributeValue
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreatingConceptInstance(TeleduTestCase):
  def testThatAttributesForConceptAreCreatedForInstance(self):
    conceptInstance = ConceptInstance.objects.create(name = self.uniqStr(), concept = self.concept)
    attribute = ConceptAttributeValue.objects.get(instance = conceptInstance, definition = self.conceptAttrDefn)
    self.assertIsNotNone(attribute)
