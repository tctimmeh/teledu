from django import forms
from django.contrib import admin
from django.forms.widgets import TextInput
from teledu.models import ConceptAttributeValue, ConceptInstance

class ConceptInstanceAdminForm(forms.ModelForm):
  class Meta:
    widgets = {'raw_value': TextInput()}

class ConceptAttributeValueInline(admin.StackedInline):
  model = ConceptAttributeValue
  form = ConceptInstanceAdminForm
  extra = 0
  can_delete = False
  fields = [('attribute', 'raw_value')]
  readonly_fields = ['attribute']

class ConceptInstanceAdmin(admin.ModelAdmin):
  search_fields = ['concept__name', 'name']
  ordering = ['concept__gameSystem__name', 'concept__name', 'name']
  list_display = ['gameSystem', 'conceptName', 'name']
  list_display_links = ['name']
  list_filter = ['concept__gameSystem__name', 'concept__name']
  inlines = [ConceptAttributeValueInline,]

admin.site.register(ConceptInstance, ConceptInstanceAdmin)

