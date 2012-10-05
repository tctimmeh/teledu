class AttributeDependentGraph(object):
  def __init__(self, attributeDefinition):
    self._definition = attributeDefinition
    self._dependentLayers = []

    self._getLayeredDependentsForAttribute()
    self._cullDuplicatesFromLayers()

  def items(self):
    for attributeSet in self._dependentLayers:
      for attribute in attributeSet:
        yield attribute

  def _getLayeredDependentsForAttribute(self):
    dependents = self._getDependentSet(self._definition)
    self._addDependencies(dependents)

    while self._dependentLayers[-1]:
      dependents = self._getDependentsOfAll(self._dependentLayers[-1])
      self._addDependencies(dependents)

  def _getDependentSet(self, attributeDefinition):
    return set(attributeDefinition.dependents.all())

  def _addDependencies(self, dependents):
    dependencyList = set()
    for dependent in dependents:
      dependencyList.add(dependent.attribute)
    self._dependentLayers.append(dependencyList)

  def _getDependentsOfAll(self, attributeDefinitions):
    allDependents = set()
    for dep in attributeDefinitions:
      dependents = self._getDependentSet(dep)
      allDependents.update(dependents)
    return allDependents

  def _cullDuplicatesFromLayers(self):
    culledLayers = []
    allDependents = set()

    for dependentLayer in reversed(self._dependentLayers):
      dependentLayer.difference_update(allDependents)
      allDependents.update(dependentLayer)
      culledLayers.insert(0, dependentLayer)

    self._dependentLayers = culledLayers

