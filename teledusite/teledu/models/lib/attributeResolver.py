class AttributeResolver(object):
  def __init__(self, modelObject):
    self.modelObject = modelObject

  def __unicode__(self):
    return unicode(self.modelObject.id)

  def __getattribute__(self, item):
    if item in ['modelObject', '_getConceptAttributeValue', '_getConceptInstance']:
      return super(AttributeResolver, self).__getattribute__(item)
    attribute = self.modelObject.getAttribute(item)
    if attribute.isConcept():
      return self._getConceptAttributeValue(attribute)
    return attribute.getValue(self.modelObject)

  def _getConceptAttributeValue(self, attribute):
    attributeValues = attribute.getAttributeValuesForInstance(self.modelObject)
    if attribute.list:
      return [self._getConceptInstance(attributeValue) for attributeValue in attributeValues]
    return self._getConceptInstance(attributeValues[0])

  def _getConceptInstance(self, attributeValue):
    from teledu.models import ConceptInstance
    conceptInstance = ConceptInstance.objects.get(pk = attributeValue.raw_value)
    return AttributeResolver(conceptInstance)

