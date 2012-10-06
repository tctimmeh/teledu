from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext, Template
from models import Character, CharacterSheet, CharacterAttribute

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

def setCharacterAttribute(request, charId, attrId):
  character = get_object_or_404(Character, id = charId)
  attribute = get_object_or_404(CharacterAttribute, id = attrId)

  value = request.POST['value']
  character.setAttributeValue(attribute.definition, value)

  return HttpResponse(value)

