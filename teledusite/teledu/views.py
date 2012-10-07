from django.core.urlresolvers import reverse
from django.forms import ModelForm, ModelChoiceField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, Template
from models import Character, CharacterSheet, CharacterAttribute, GameSystem, CharacterAttributeDefinition

def welcome(request):
  return render(request, 'welcome.html')

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

class CharacterForm(ModelForm):
  gameSystem = ModelChoiceField(queryset = GameSystem.objects.all(), label = 'Game System')
  class Meta:
    model = Character
    exclude = ('attributes')

def createCharacter(request):
  if request.method == 'POST':
    form = CharacterForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      character = Character.create(data['gameSystem'], data['name'])
      return HttpResponseRedirect(reverse(charSheet, kwargs = {'charId': character.id}))
  else:
    form = CharacterForm()

  return render(request, 'createCharacter.html', {'form': form})

