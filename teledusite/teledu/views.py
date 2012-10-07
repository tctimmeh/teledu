from django.core.urlresolvers import reverse
from django.forms import ModelForm, ModelChoiceField, Form, BooleanField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, Template
from models import Character, CharacterSheet, CharacterAttribute, GameSystem

def welcome(request):
  return render(request, 'welcome.html', {'characters': Character.objects.all()})

def charSheet(request, charId, json):
  character = get_object_or_404(Character, id = charId)
  if request.method == 'DELETE':
    character.delete()
    return HttpResponse()

  if json:
    return HttpResponse(character.serialize())

  sheetTemplates = CharacterSheet.objects.filter(gameSystem = character.gameSystem)
  if sheetTemplates:
    sheetTemplate = sheetTemplates[0].template
  else:
    sheetTemplate = r'''<p>
  <b>Name</b>: {{ character.name }}
</p>
{% for attribute in character.attributes.all %}
  <p>
    <b>{{ attribute.name }}</b>: {% char_attr attribute %}
  </p>
{% endfor %}'''

  templateHeader =  '''{% extends "characterSheet.html" %}
{% load character %}
{% block characterSheet %}
'''
  templateFooter = '''
{% endblock %}
'''
  templateString = '%s%s%s' % (templateHeader, sheetTemplate, templateFooter)
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

def deleteCharacter(request, charId):
  character = get_object_or_404(Character, id = charId)
  if request.POST.get('confirm', False):
    character.delete()
    return HttpResponseRedirect(reverse(welcome))
  return render(request, 'deleteCharacter.html', {'character': character})

