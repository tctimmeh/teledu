import json
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ModelChoiceField
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, Template
from django.template.loader import get_template
from models import Character, CharacterSheet, GameSystem, CharacterAttributeDefinition, ConceptInstance, CharacterAttribute, DataType

def welcome(request):
  return render(request, 'welcome.html', {'characters': Character.objects.all()})

def compileCustomSheetForCharacter(templateCode):
  templateHeader =  '''{% extends "characterSheet.html" %}
{% load character %}
{% block characterSheet %}
'''
  templateFooter = '''
{% endblock %}
'''
  templateString = '%s%s%s' % (templateHeader, templateCode, templateFooter)
  return Template(templateString)

def charSheet(request, charId, json):
  character = get_object_or_404(Character, id = charId)
  if request.method == 'DELETE':
    character.delete()
    return HttpResponse()

  if json:
    return HttpResponse(character.serialize())

  sheetTemplates = CharacterSheet.objects.filter(gameSystem = character.gameSystem)
  if sheetTemplates:
    template = compileCustomSheetForCharacter(sheetTemplates[0].template)
  else:
    template = get_template("defaultCharacterTemplate.html")

  context = RequestContext(request)
  context.update({
    'character': character,
  })
  return HttpResponse(template.render(context))

def setCharacterAttribute(request, charId, attrId):
  character = get_object_or_404(Character, id = charId)
  attribute = get_object_or_404(CharacterAttributeDefinition, id = attrId)

  value = request.POST['value']
  changedAttributes = character.setAttributeValue(attribute, value)

  return HttpResponse(json.dumps(changedAttributes))

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

def getCharacterAttributeChoices(request, charId, attrId):
  character = get_object_or_404(Character, id = charId)
  try:
    definition = character.attributes.get(id = attrId)
  except CharacterAttributeDefinition.DoesNotExist:
    raise Http404()

  if definition.dataType.id != DataType.CONCEPT:
    return HttpResponse('')

  conceptInstances = ConceptInstance.objects.filter(concept = definition.concept)
  out = {}
  for instance in conceptInstances:
    out[instance.id] = instance.name
  out['selected'] = CharacterAttribute.objects.get(character = character, definition = definition).raw_value

  return HttpResponse(json.dumps(out))

