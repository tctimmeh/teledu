from teledu.models import ConceptInstance, ConceptAttributeValue
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenCreatingConceptInstance(TeleduTestCase):
  def testThatAttributeValuesForConceptAreCreatedForInstance(self):
    conceptInstance = ConceptInstance.objects.create(name = self.uniqStr(), concept = self.concept)
    attribute = ConceptAttributeValue.objects.get(instance = conceptInstance, attribute = self.conceptAttr)
    self.assertIsNotNone(attribute)

  def testThatListAttributesGetNoDefaultAttributeValues(self):
    self.conceptAttr.list = True
    self.conceptAttr.save()

    conceptInstance = ConceptInstance.objects.create(name = self.uniqStr(), concept = self.concept)
    attribute = ConceptAttributeValue.objects.filter(instance = conceptInstance, attribute = self.conceptAttr)
    self.assertEqual(len(attribute), 0)

