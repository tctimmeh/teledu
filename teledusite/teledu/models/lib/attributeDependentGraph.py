from django.db.models import Model

def combineAttributeGraphs(*attributeSets):
  out = set()
  for attributeSet in attributeSets:
    if attributeSet is None:
      continue
    out.update(attributeSet)
  return out

class AttributeDependentGraph(object):
  def __init__(self, attribute):
    if isinstance(attribute, Model):
      attribute = [attribute]

    self._dependentLayers = self._buildDependentsLayers(attribute)
    self._cullDuplicatesFromLayers()

  def items(self):
    for attributeSet in self._dependentLayers:
      for attribute in attributeSet:
        yield attribute

  def _buildDependentsLayers(self, attributes):
    graphs = []

    for attribute in attributes:
      graphs.append(self._buildLayersForAttribute(attribute))

    layers = map(combineAttributeGraphs, *graphs)
    return layers

  def _buildLayersForAttribute(self, attribute):
    layers = []
    dependents = self._getDependentSet(attribute)
    self._addDependencies(layers, dependents)

    while layers[-1]:
      dependents = self._getDependentsOfAll(layers[-1])
      self._addDependencies(layers, dependents)

    return layers

  def _getDependentSet(self, attribute):
    return set(attribute.dependents.all())

  def _addDependencies(self, layers, dependents):
    dependencyList = set()
    for dependent in dependents:
      dependencyList.add(dependent.attribute)
    layers.append(dependencyList)

  def _getDependentsOfAll(self, attributes):
    allDependents = set()
    for dep in attributes:
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


