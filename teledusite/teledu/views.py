from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, Template
from models import Character, CharacterSheet

def hello(request):
  return HttpResponse('Hello, Teledu!')

def charSheet(request, charId, json):
  character = get_object_or_404(Character, id = charId)
  if json:
    return HttpResponse(character.serialize())

  sheetTemplate = CharacterSheet.objects.filter(gameSystem = character.gameSystem)[0]

  templateHeader =  '''{% extends "characterSheet.html" %}
{% load character %}
{% block characterSheet %}
'''
  templateFooter = '''
{% endblock %}
'''
  templateString = '%s%s%s' % (templateHeader, sheetTemplate.template, templateFooter)
  context = RequestContext(request)
  context.update({
    'character': character,
  })
  template = Template(templateString)
  output = template.render(context)

  return HttpResponse(output)
