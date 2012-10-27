import random
from teledu.tests.teleduTestCase import TeleduTestCase
from teledu.models import CharacterAttributeValue

class WhenSettingCharacterAttributeValue(TeleduTestCase):
  def getAttrValue(self, attribute):
    return int(CharacterAttributeValue.objects.get(character = self.character, attribute = attribute).raw_value)
    
  def testThatAttributeHasNewValue(self):
    attrA = self.addAttributeToCharacter()

    expected = random.randint(2, 20)
    self.character.setAttributeValue(attrA, expected)

    actual = self.getAttrValue(attrA)
    self.assertEqual(actual, expected)

  def testThatDirectDependentsCalculateNewValues(self):
    # A <- B
    attrA = self.addAttributeToCharacter(type = 'integer')
    attrB = self.addAttributeToCharacter([attrA], 'result = character.%s + 1' % attrA.name, type = 'integer')

    expected = random.randint(2, 20)
    self.character.setAttributeValue(attrA, expected)
    expected += 1

    actual = int(CharacterAttributeValue.objects.get(character = self.character, attribute = attrB).raw_value)
    self.assertEqual(actual, expected)

  def testThatIndirectDependentsCalculateNewValues(self):
    # A <- B <- C
    attrA = self.addAttributeToCharacter(type = 'integer')
    attrB = self.addAttributeToCharacter([attrA], 'result = character.%s + 1' % attrA.name, type = 'integer')
    attrC = self.addAttributeToCharacter([attrB], 'result = character.%s + 1' % attrB.name, type = 'integer')

    expected = random.randint(2, 20)
    self.character.setAttributeValue(attrA, expected)
    expected += 2

    actual = int(CharacterAttributeValue.objects.get(character = self.character, attribute = attrC).raw_value)
    self.assertEqual(actual, expected)

  def testThatDiamondDependentsCalculateNewValues(self):
    #   B
    #  / \
    # A   D
    #  \ /
    #   C
    attrA = self.addAttributeToCharacter(type = 'integer')
    attrB = self.addAttributeToCharacter([attrA], 'result = character.%s + 1' % attrA.name, type = 'integer')
    attrC = self.addAttributeToCharacter([attrA], 'result = character.%s + 2' % attrA.name, type = 'integer')
    attrD = self.addAttributeToCharacter([attrB, attrC], 'result = character.%s * character.%s' % (attrB.name, attrC.name), type = 'integer')

    setValue = random.randint(2, 20)
    self.character.setAttributeValue(attrA, setValue)
    expected = (setValue + 1) * (setValue + 2)

    actual = int(CharacterAttributeValue.objects.get(character = self.character, attribute = attrD).raw_value)
    self.assertEqual(actual, expected)

  def testThatGrandchildDependentsCalculateNewValues(self):
    #   B
    #  / \
    # A<--C
    attrA = self.addAttributeToCharacter(type = 'integer')
    attrB = self.addAttributeToCharacter([attrA], 'result = character.%s + 1' % attrA.name, type = 'integer')
    attrC = self.addAttributeToCharacter([attrA, attrB], 'result = character.%s * character.%s' % (attrA.name, attrB.name), type = 'integer')

    setValue = random.randint(2, 20)
    self.character.setAttributeValue(attrA, setValue)
    expected = setValue * (setValue + 1)

    actual = int(CharacterAttributeValue.objects.get(character = self.character, attribute = attrC).raw_value)
    self.assertEqual(actual, expected)

