from django import forms
from django.contrib import admin
from django.forms.widgets import TextInput
from .models import GameSystem, CharacterAttributeDefinition, Character, CharacterAttribute, CharacterSheet

class CharacterAttributeForm(forms.ModelForm):
  class Meta:
    widgets = {'value': TextInput()}

class CharacterAttributeInline(admin.StackedInline):
  model = CharacterAttribute
  form = CharacterAttributeForm
  extra = 0
  can_delete = False
  fields = [('definition', 'value')]
  readonly_fields = ['definition']

class CharacterAdmin(admin.ModelAdmin):
  inlines = [CharacterAttributeInline,]

admin.site.register(GameSystem)
admin.site.register(Character, CharacterAdmin)
admin.site.register(CharacterAttributeDefinition)
admin.site.register(CharacterSheet)

