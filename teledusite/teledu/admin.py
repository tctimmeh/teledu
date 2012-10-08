from django import forms
from django.contrib import admin
from django.forms.widgets import TextInput
from .models import GameSystem, CharacterAttributeDefinition, Character, CharacterAttribute, CharacterSheet
from teledu.models.characterAttributeDependency import CharacterAttributeDependency

class CharacterAttributeForm(forms.ModelForm):
  class Meta:
    widgets = {'raw_value': TextInput()}

class CharacterAttributeInline(admin.StackedInline):
  model = CharacterAttribute
  form = CharacterAttributeForm
  extra = 0
  can_delete = False
  fields = [('definition', 'raw_value')]

class CharacterAdmin(admin.ModelAdmin):
  inlines = [CharacterAttributeInline,]
  actions = ['recalculateCharacters']

  def recalculateCharacters(admin, request, querySet):
    for character in querySet:
      character.recalculateAllAttributes()
    admin.message_user(request, "%s successfully recalculated" % len(querySet))
  recalculateCharacters.short_description = 'Recalculate attributes for selected characters'

class CharacterAttributeDependencyInline(admin.StackedInline):
  model = CharacterAttributeDependency
  fk_name = 'attribute'
  extra = 0

class CharacterAttributeDefinitionAdmin(admin.ModelAdmin):
  search_fields = ['name']
  ordering = ['gameSystem__name', 'name']
  list_display = ['gameSystem', 'name', 'dataType', 'default']
  list_display_links = ['name']
  list_filter = ['gameSystem']
  list_editable = ['dataType', 'default']
  inlines = [CharacterAttributeDependencyInline,]

admin.site.register(GameSystem)
admin.site.register(Character, CharacterAdmin)
admin.site.register(CharacterAttributeDefinition, CharacterAttributeDefinitionAdmin)
admin.site.register(CharacterSheet)

