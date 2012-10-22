
class AttributeResolver(object):
  def __init__(self, character):
    self.character = character

  def getAttributeValue(self, expression):
    from teledu.models import CharacterAttributeDefinition, CharacterAttribute, ConceptInstance, ConceptAttributeDefinition, ConceptInstanceAttribute

    parts = expression.split('.')
    if len(parts) < 2:
      return self.character.getAttributeValue(expression)

    definition = CharacterAttributeDefinition.objects.get(gameSystem = self.character.gameSystem, name = parts[0])
    attribute = CharacterAttribute.objects.get(definition = definition, character = self.character)
    conceptInstance = ConceptInstance.objects.get(pk = attribute.raw_value)
    conceptAttrDefn = ConceptAttributeDefinition.objects.get(concept = definition.valueConcept, name = parts[1])
    conceptAttribute = ConceptInstanceAttribute.objects.get(definition = conceptAttrDefn, instance = conceptInstance)

    return conceptAttribute.raw_value
