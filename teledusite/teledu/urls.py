from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  url(r'^$', 'teledu.views.hello'),
  url(r'^character/(?P<charId>\d+?)(?P<json>\.json)?$', 'teledu.views.charSheet'),
  url(r'^character/(?P<charId>\d+?)/setAttribute$', 'teledu.views.setCharacterAttribute'),
)

