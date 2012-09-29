from django.db import models

class GameSystem(models.Model):
  name = models.CharField(max_length = 100)

  def __unicode__(self):
    return self.name

class CharacterAttributeDefinition(models.Model):
  gameSystem = models.ForeignKey(GameSystem)
  name = models.CharField(max_length = 30)

  def __unicode__(self):
    return self.name

class Character(models.Model):
  name = models.CharField(max_length = 50)
  attributes = models.ManyToManyField(CharacterAttributeDefinition, through = 'CharacterAttribute')

  def __unicode__(self):
    return self.name

class CharacterAttribute(models.Model):
  character = models.ForeignKey(Character)
  attribute = models.ForeignKey(CharacterAttributeDefinition)
  value = models.TextField(null = True, blank = True, default = None)

  def __unicode__(self):
    return '%s [%s] = [%s]' % (self.character.name, self.attribute.name, self.value)

