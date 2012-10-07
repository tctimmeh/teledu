import random
from teledu.tests.teleduTestCase import TeleduTestCase
from teledu.models import CharacterAttribute, CharacterAttributeDependency

class WhenSettingCharacterAttributeValue(TeleduTestCase):
  def addAttrDefinition(self, dependencies = [], calcFunction = None):
    attr = self.createAttrDefinition(calcFunction = calcFunction)
    self.createAttrForCharacter(attrDefinition = attr)
    for dependency in dependencies:
      CharacterAttributeDependency.objects.create(attribute = attr, dependency = dependency)
    return attr

  def getAttrValue(self, attrDefn):
    return int(CharacterAttribute.objects.get(character = self.character, definition = attrDefn).value)
    
  def testThatAttributeHasNewValue(self):
    attrA = self.addAttrDefinition()

    expected = random.randint(2, 20)
    self.character.setAttributeValue(attrA, expected)

    actual = self.getAttrValue(attrA)
    self.assertEqual(actual, expected)

  def testThatDirectDependentsCalculateNewValues(self):
    # A <- B
    attrA = self.addAttrDefinition()
    attrB = self.addAttrDefinition([attrA], 'result = int(attr("%s")) + 1' % attrA.name)

    expected = random.randint(2, 20)
    self.character.setAttributeValue(attrA, expected)
    expected += 1

    actual = int(CharacterAttribute.objects.get(character = self.character, definition = attrB).value)
    self.assertEqual(actual, expected)

  def testThatIndirectDependentsCalculateNewValues(self):
    # A <- B <- C
    attrA = self.addAttrDefinition()
    attrB = self.addAttrDefinition([attrA], 'result = int(attr("%s")) + 1' % attrA.name)
    attrC = self.addAttrDefinition([attrB], 'result = int(attr("%s")) + 1' % attrB.name)

    expected = random.randint(2, 20)
    self.character.setAttributeValue(attrA, expected)
    expected += 2

    actual = int(CharacterAttribute.objects.get(character = self.character, definition = attrC).value)
    self.assertEqual(actual, expected)

  def testThatDiamondDependentsCalculateNewValues(self):
    #   B
    #  / \
    # A   D
    #  \ /
    #   C
    attrA = self.addAttrDefinition()
    attrB = self.addAttrDefinition([attrA], 'result = int(attr("%s")) + 1' % attrA.name)
    attrC = self.addAttrDefinition([attrA], 'result = int(attr("%s")) + 2' % attrA.name)
    attrD = self.addAttrDefinition([attrB, attrC], 'result = int(attr("%s")) * int(attr("%s"))' % (attrB.name, attrC.name))

    setValue = random.randint(2, 20)
    self.character.setAttributeValue(attrA, setValue)
    expected = (setValue + 1) * (setValue + 2)

    actual = int(CharacterAttribute.objects.get(character = self.character, definition = attrD).value)
    self.assertEqual(actual, expected)

  def testThatGrandchildDependentsCalculateNewValues(self):
    #   B
    #  / \
    # A<--C
    attrA = self.addAttrDefinition()
    attrB = self.addAttrDefinition([attrA], 'result = int(attr("%s")) + 1' % attrA.name)
    attrC = self.addAttrDefinition([attrA, attrB], 'result = int(attr("%s")) * int(attr("%s"))' % (attrA.name, attrB.name))

    setValue = random.randint(2, 20)
    self.character.setAttributeValue(attrA, setValue)
    expected = (setValue) * (setValue + 1)

    actual = int(CharacterAttribute.objects.get(character = self.character, definition = attrC).value)
    self.assertEqual(actual, expected)
