from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  url(r'^$', 'teledu.views.hello'),
  url(r'^character/(?P<charId>.+?)(?P<json>\.json)?$', 'teledu.views.charSheet')
)

