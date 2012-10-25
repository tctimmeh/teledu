from django.contrib import admin
from teledu.models import ConceptAttribute

class ConceptAttributeAdmin(admin.ModelAdmin):
  search_fields = ['concept__name', 'name']
  ordering = ['concept__gameSystem__name', 'concept__name', 'name']
  list_display = ['gameSystem', 'conceptName', 'name', 'dataType']
  list_display_links = ['name']
  list_filter = ['concept__gameSystem__name', 'concept__name']
  list_editable = ['dataType']

admin.site.register(ConceptAttribute, ConceptAttributeAdmin)

