import json
from django.core import serializers
from django.db import models
from .characterAttributeDefinition import CharacterAttributeDefinition

class Character(models.Model):
  name = models.CharField(max_length = 50)
  attributes = models.ManyToManyField(CharacterAttributeDefinition, through = 'CharacterAttribute')

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return self.name

  def serialize(self):
    attributes = CharacterAttribute.objects.filter(character = self)
    return json.dumps({
      'id': self.id,
      'name': self.name,
      'attributes': [attribute.asDict() for attribute in attributes],
    })

  @property
  def gameSystem(self):
    return self.attributes.all()[0].gameSystem

  def getAttribute(self, id):
    return CharacterAttribute.objects.get(character = self, attribute = id).value

from .characterAttribute import CharacterAttribute

