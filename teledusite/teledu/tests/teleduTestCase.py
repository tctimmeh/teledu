import random
from django.test import TestCase
from teledu.tests.testHelpers import TestHelpers

random.seed(0x5ADB0075)

class TeleduTestCase(TestCase, TestHelpers):
  urls = 'teledu.urls'
  fixtures = ['initial_data']

  def setUp(self):
    self.gameSystem = self.createGameSystem()
    self.character = self.createCharacter()
    self.charAttr = self.createAttribute(self.gameSystem)
    self.charAttrValue = self.createAttributeValueForCharacter(self.charAttr, self.character, self.uniqStr())
    self.charSheetTemplate = self.createCharacterSheetTemplate()
    self.concept = self.createConcept()
    self.conceptAttr = self.createConceptAttr()

