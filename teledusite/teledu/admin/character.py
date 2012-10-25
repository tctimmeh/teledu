from django import forms
from django.contrib import admin
from django.forms.widgets import TextInput
from teledu.models import Character, CharacterAttributeValue

class CharacterAttributeForm(forms.ModelForm):
  class Meta:
    widgets = {'raw_value': TextInput()}

class CharacterAttributeValueInline(admin.StackedInline):
  model = CharacterAttributeValue
  form = CharacterAttributeForm
  extra = 0
  can_delete = False
  fields = [('definition', 'raw_value')]
  readonly_fields = ['definition']

class CharacterAdmin(admin.ModelAdmin):
  inlines = [CharacterAttributeValueInline,]
  actions = ['recalculateCharacters', "applyCurrentCharacterAttributesToAllCharacters"]

  def recalculateCharacters(admin, request, querySet):
    for character in querySet:
      character.recalculateAllAttributes()
    admin.message_user(request, "%s successfully recalculated" % len(querySet))
  recalculateCharacters.short_description = 'Recalculate attributes for selected characters'

  def applyCurrentCharacterAttributesToAllCharacters(self, request, querySet):
    for character in querySet:
      character.addMissingCharacterAttributeDefinitions()
    self.message_user(request, "You successfully applied all current rules to %s characters" % len(querySet))
  applyCurrentCharacterAttributesToAllCharacters.short_description = "Apply all current character attributes to selected characters"

admin.site.register(Character, CharacterAdmin)

