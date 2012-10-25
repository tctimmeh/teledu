
class AttributeResolver(object):
  def __init__(self, character):
    self.character = character

  def getAttributeValue(self, expression):
    from teledu.models import CharacterAttribute, CharacterAttributeValue, ConceptInstance, ConceptAttribute, ConceptAttributeValue

    parts = expression.split('.')
    if len(parts) < 2:
      return self.character.getAttributeValue(expression)

    attribute = CharacterAttribute.objects.get(gameSystem = self.character.gameSystem, name = parts[0])
    attributeValue = CharacterAttributeValue.objects.get(attribute = attribute, character = self.character)
    conceptInstance = ConceptInstance.objects.get(pk = attributeValue.raw_value)
    conceptAttribute = ConceptAttribute.objects.get(concept = attribute.valueConcept, name = parts[1])
    conceptAttributeValue = ConceptAttributeValue.objects.get(attribute = conceptAttribute, instance = conceptInstance)

    return conceptAttributeValue.raw_value
