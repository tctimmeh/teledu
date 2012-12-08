from attributeResolver import AttributeResolver

class CalculationFunction(object):
  def __init__(self, definition, attribute, operand):
    self.definition = definition
    self.attribute = attribute
    self.operand = operand
    self.result = None

  def execute(self):
    attributeValue = self.attribute.getAttributesForInstance(self.operand)[0]
    if self.definition:
      newValue = self._execCalcFunction()
      attributeValue.raw_value = unicode(newValue)
      attributeValue.save()

    self.result = attributeValue.value

  def _execCalcFunction(self):
    scope = {
      'character': AttributeResolver(self.operand),
      'result': None
    }
    exec self.definition in scope
    return scope['result']

