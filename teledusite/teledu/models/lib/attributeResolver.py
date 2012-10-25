
class AttributeResolver(object):
  def __init__(self, character):
    self.character = character

  def getAttributeValue(self, expression):
    from teledu.models import CharacterAttribute, CharacterAttributeValue, ConceptInstance, ConceptAttribute, ConceptAttributeValue

    parts = expression.split('.')
    if len(parts) < 2:
      return self.character.getAttributeValue(expression)

    definition = CharacterAttribute.objects.get(gameSystem = self.character.gameSystem, name = parts[0])
    attribute = CharacterAttributeValue.objects.get(definition = definition, character = self.character)
    conceptInstance = ConceptInstance.objects.get(pk = attribute.raw_value)
    conceptAttrDefn = ConceptAttribute.objects.get(concept = definition.valueConcept, name = parts[1])
    conceptAttribute = ConceptAttributeValue.objects.get(definition = conceptAttrDefn, instance = conceptInstance)

    return conceptAttribute.raw_value
