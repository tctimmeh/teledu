import json
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenSerializing(TeleduTestCase):
  def testThatOutputIsValidJson(self):
    json.loads(self.character.serialize())
