from django.db import models

class GameSystem(models.Model):
  name = models.CharField(max_length = 100, unique = True)

  class Meta:
    app_label = 'teledu'

  def __unicode__(self):
    return self.name

