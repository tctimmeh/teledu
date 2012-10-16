from teledu.models.lib import AttributeDependentGraph
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingAttributes(TeleduTestCase):
  def assertGraphEqual(self, actualList, expectedLayers):
    for expectedLayer in expectedLayers:
      actualLayer = []
      for attribute in expectedLayer:
        actualLayer.append(actualList.pop(0))
      expectedLayer.sort(cmp = lambda x, y: cmp(unicode(x), unicode(y)))
      actualLayer.sort(cmp = lambda x, y: cmp(unicode(x), unicode(y)))
      self.assertEqual(actualLayer, expectedLayer)

  def testThatDependentsAreListedAfterDependencies(self):
    attrA = self.addAttrDefnToCharacter()
    attrB = self.addAttrDefnToCharacter([attrA])
    attrC = self.addAttrDefnToCharacter([attrB])
    expected = [attrB, attrC]

    graph = AttributeDependentGraph(attrA)
    actual = list(graph.items())
    self.assertEqual(actual, expected)

  def testThatDependentsOfManyAttributesAreListedAtTheirLatestPosition(self):
    attrA = self.addAttrDefnToCharacter()
    attrB = self.addAttrDefnToCharacter([attrA])
    attrC = self.addAttrDefnToCharacter([attrA, attrB])
    attrD = self.addAttrDefnToCharacter([attrC])
    expected = [attrB, attrC, attrD]

    graph = AttributeDependentGraph(attrA)
    actual = list(graph.items())
    self.assertEqual(actual, expected)

  def testThatDependentsOfAllAttributesAreListed(self):
    pathAFirst = self.addAttrDefnToCharacter()
    pathASecond = self.addAttrDefnToCharacter([pathAFirst])
    pathAThird = self.addAttrDefnToCharacter([pathASecond])
    pathBFirst = self.addAttrDefnToCharacter()
    pathBSecond = self.addAttrDefnToCharacter([pathBFirst])
    pathBThird = self.addAttrDefnToCharacter([pathBSecond])
    bottomAttr = self.addAttrDefnToCharacter([pathASecond, pathBThird])
    expected = [[pathASecond, pathBSecond], [pathAThird, pathBThird], [bottomAttr]]

    graph = AttributeDependentGraph([pathAFirst, pathBFirst])
    actual = list(graph.items())

    self.assertGraphEqual(actual, expected)

