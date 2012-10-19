from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  url(r'^$', 'teledu.views.welcome'),
  url(r'^character$', 'teledu.views.createCharacter'),
  url(r'^character/(?P<charId>\d+?)(?P<json>\.json)?$', 'teledu.views.charSheet'),
  url(r'^character/(?P<charId>\d+?)/delete$', 'teledu.views.deleteCharacter'),
  url(r'^character/(?P<charId>\d+?)/attribute/(?P<attrId>\d+?)$', 'teledu.views.setCharacterAttribute'),
  url(r'^character/(?P<charId>\d+?)/attribute/(?P<attrId>\d+?)/choices$', 'teledu.views.getCharacterAttributeChoices'),
)

