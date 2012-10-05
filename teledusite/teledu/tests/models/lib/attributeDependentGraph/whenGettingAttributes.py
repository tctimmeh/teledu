from teledu.models import CharacterAttributeDependency
from teledu.models.lib import AttributeDependentGraph
from teledu.tests.teleduTestCase import TeleduTestCase

class WhenGettingAttributes(TeleduTestCase):
  def addAttrDefinition(self, dependencies = [], calcFunction = None):
    attr = self.createAttrDefinition(calcFunction = calcFunction)
    self.createAttrForCharacter(attrDefinition = attr)
    for dependency in dependencies:
      CharacterAttributeDependency.objects.create(attribute = attr, dependency = dependency)
    return attr

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

