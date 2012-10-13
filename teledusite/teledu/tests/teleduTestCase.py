import random
from django.test import TestCase
from teledu.tests.testHelpers import TestHelpers

random.seed(0x5ADB0075)

class TeleduTestCase(TestCase, TestHelpers):
  urls = 'teledu.urls'

  def setUp(self):
    self.gameSystem = self.createGameSystem()
    self.attributeDefinition = self.createAttrDefinition(self.gameSystem)
    self.character = self.createCharacter()
    self.attributeValue = self.uniqStr()
    self.charAttr = self.createAttrForCharacter(self.attributeDefinition, self.character, self.attributeValue)
    self.charSheetTemplate = self.createCharacterSheetTemplate()
    self.concept = self.createConcept()
    self.conceptAttrDefn = self.createConceptAttrDefn()

