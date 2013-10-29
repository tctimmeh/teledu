from attributeResolver import AttributeResolver

class CalculationFunction(object):
  def __init__(self, definition, attribute, operand):
    self.definition = definition
    self.attribute = attribute
    self.operand = operand
    self.result = None

  def execute(self):
    if self.definition:
      newValue = self._execCalcFunction()
      self.attribute.setRawValue(self.operand, newValue)

    self.result = self.attribute.getValue(self.operand)

  def _execCalcFunction(self):
    from teledu.models.lib.conceptResolver import ConceptResolver
    scope = {
      'character': AttributeResolver(self.operand),
      'concept': ConceptResolver(self.operand.gameSystem),
      'result': None
    }
    exec self.definition in scope
    return scope['result']

