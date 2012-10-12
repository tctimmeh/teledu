from django import forms
from django.contrib import admin
from django.forms.widgets import TextInput
from teledu.models import CharacterAttribute, Character

class CharacterAttributeForm(forms.ModelForm):
  class Meta:
    widgets = {'raw_value': TextInput()}

class CharacterAttributeInline(admin.StackedInline):
  model = CharacterAttribute
  form = CharacterAttributeForm
  extra = 0
  can_delete = False
  fields = [('definition', 'raw_value')]
  readonly_fields = ['definition']

class CharacterAdmin(admin.ModelAdmin):
  inlines = [CharacterAttributeInline,]
  actions = ['recalculateCharacters']

  def recalculateCharacters(admin, request, querySet):
    for character in querySet:
      character.recalculateAllAttributes()
    admin.message_user(request, "%s successfully recalculated" % len(querySet))
  recalculateCharacters.short_description = 'Recalculate attributes for selected characters'

admin.site.register(Character, CharacterAdmin)

