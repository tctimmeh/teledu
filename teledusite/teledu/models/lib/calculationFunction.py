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
      #attributeValue = self.attribute.getAttributeValuesForInstance(self.operand)[0]
      #attributeValue.raw_value = unicode(newValue)
      #attributeValue.save()

    self.result = self.attribute.getValue(self.operand)

  def _execCalcFunction(self):
    scope = {
      'character': AttributeResolver(self.operand),
      'result': None
    }
    exec self.definition in scope
    return scope['result']

