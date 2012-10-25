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
    attrA = self.addAttributeToCharacter()
    attrB = self.addAttributeToCharacter([attrA])
    attrC = self.addAttributeToCharacter([attrB])
    expected = [attrB, attrC]

    graph = AttributeDependentGraph(attrA)
    actual = list(graph.items())
    self.assertEqual(actual, expected)

  def testThatDependentsOfManyAttributesAreListedAtTheirLatestPosition(self):
    attrA = self.addAttributeToCharacter()
    attrB = self.addAttributeToCharacter([attrA])
    attrC = self.addAttributeToCharacter([attrA, attrB])
    attrD = self.addAttributeToCharacter([attrC])
    expected = [attrB, attrC, attrD]

    graph = AttributeDependentGraph(attrA)
    actual = list(graph.items())
    self.assertEqual(actual, expected)

  def testThatDependentsOfAllAttributesAreListed(self):
    pathAFirst = self.addAttributeToCharacter()
    pathASecond = self.addAttributeToCharacter([pathAFirst])
    pathAThird = self.addAttributeToCharacter([pathASecond])
    pathBFirst = self.addAttributeToCharacter()
    pathBSecond = self.addAttributeToCharacter([pathBFirst])
    pathBThird = self.addAttributeToCharacter([pathBSecond])
    bottomAttr = self.addAttributeToCharacter([pathASecond, pathBThird])
    expected = [[pathASecond, pathBSecond], [pathAThird, pathBThird], [bottomAttr]]

    graph = AttributeDependentGraph([pathAFirst, pathBFirst])
    actual = list(graph.items())

    self.assertGraphEqual(actual, expected)

