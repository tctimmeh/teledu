from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingAttributeValue(TeleduTestCase):
  def setUp(self):
    super(WhenGettingAttributeValue, self).setUp()
    self.expected = self.uniqStr()
    self.attribute = self.createConceptAttr(self.concept)
    self.instance = self.createConceptInstance(attributes = {self.attribute: self.expected})

  def testGettingByAttributeIdReturnsAttributeValue(self):
    actual = self.instance.getAttributeValue(self.attribute.id)
    self.assertEqual(actual, self.expected)

  def testGettingByAttributeInstanceReturnsAttributeValue(self):
    actual = self.instance.getAttributeValue(self.attribute)
    self.assertEqual(actual, self.expected)

  def testGettingByAttributeNameReturnsAttributeValue(self):
    actual = self.instance.getAttributeValue(self.attribute.name)
    self.assertEqual(actual, self.expected)

  def testConceptInstanceNameIsReturnedForConceptAttributes(self):
    otherConcept = self.createConcept()
    expectedInstance = self.createConceptInstance(otherConcept)

    attribute = self.createConceptAttr(self.concept, type = 'concept', valueConcept = otherConcept)
    instance = self.createConceptInstance(self.concept, attributes = {attribute: expectedInstance})

    actual = instance.getAttributeValue(attribute)
    self.assertEqual(actual, expectedInstance.name)
