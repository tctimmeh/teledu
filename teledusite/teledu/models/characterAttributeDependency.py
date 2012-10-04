from django.db import models
from characterAttributeDefinition import CharacterAttributeDefinition

class CharacterAttributeDependency(models.Model):
  attribute = models.ForeignKey(CharacterAttributeDefinition, related_name = 'dependencies')
  dependency = models.ForeignKey(CharacterAttributeDefinition, related_name = 'dependents')

  class Meta:
    app_label = 'teledu'
    unique_together = (('attribute', 'dependency'))

  def __unicode__(self):
    return '%s --> %s' % (self.attribute.name, self.dependency.name)

