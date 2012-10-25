from django.db import models
from characterAttribute import CharacterAttribute

class CharacterAttributeDependency(models.Model):
  attribute = models.ForeignKey(CharacterAttribute, related_name = 'dependencies')
  dependency = models.ForeignKey(CharacterAttribute, related_name = 'dependents')

  class Meta:
    app_label = 'teledu'
    unique_together = (('attribute', 'dependency'))

  def __unicode__(self):
    return '%s --> %s' % (self.attribute.name, self.dependency.name)

