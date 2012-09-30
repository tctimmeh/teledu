from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, Template
from models import Character

def hello(request):
  return HttpResponse('Hello, Teledu!')

def charSheet(request, charId):
  character = get_object_or_404(Character, id = charId)

  templateHeader =  '''{% extends "characterSheet.html" %}
{% load character %}
{% block characterSheet %}
'''

  templateData = '''<p>
  <b>Name</b>: {{ character.name }}
</p>
{% for attribute in character.attributes.all %}
  <p>
    <b>{{ attribute.name }}</b>: {{ character|charAttr:attribute }}
  </p>
{% endfor %}'''

  templateFooter = '''
{% endblock %}
'''
  templateString = '%s%s%s' % (templateHeader, templateData, templateFooter)
  context = RequestContext(request)
  context.update({
    'character': character,
  })
  template = Template(templateString)
  output = template.render(context)

  return HttpResponse(output)
  render()
