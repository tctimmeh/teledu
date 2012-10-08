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
    attrA = self.addAttrDefinition()
    attrB = self.addAttrDefinition([attrA])
    attrC = self.addAttrDefinition([attrB])
    expected = [attrB, attrC]

    graph = AttributeDependentGraph(attrA)
    actual = list(graph.items())
    self.assertEqual(actual, expected)

  def testThatDependentsOfManyAttributesAreListedAtTheirLatestPosition(self):
    attrA = self.addAttrDefinition()
    attrB = self.addAttrDefinition([attrA])
    attrC = self.addAttrDefinition([attrA, attrB])
    attrD = self.addAttrDefinition([attrC])
    expected = [attrB, attrC, attrD]

    graph = AttributeDependentGraph(attrA)
    actual = list(graph.items())
    self.assertEqual(actual, expected)

  def testThatDependentsOfAllAttributesAreListed(self):
    pathAFirst = self.addAttrDefinition()
    pathASecond = self.addAttrDefinition([pathAFirst])
    pathAThird = self.addAttrDefinition([pathASecond])
    pathBFirst = self.addAttrDefinition()
    pathBSecond = self.addAttrDefinition([pathBFirst])
    pathBThird = self.addAttrDefinition([pathBSecond])
    bottomAttr = self.addAttrDefinition([pathASecond, pathBThird])
    expected = [[pathASecond, pathBSecond], [pathAThird, pathBThird], [bottomAttr]]

    graph = AttributeDependentGraph([pathAFirst, pathBFirst])
    actual = list(graph.items())

    self.assertGraphEqual(actual, expected)

