from django.contrib import admin
from teledu.models import Concept

class GameSystemConceptAdmin(admin.ModelAdmin):
  search_fields = ['name']
  ordering = ['gameSystem', 'name']
  list_display = ['gameSystem', 'name']
  list_display_links = ['name']
  list_filter = ['gameSystem']

admin.site.register(Concept, GameSystemConceptAdmin)

