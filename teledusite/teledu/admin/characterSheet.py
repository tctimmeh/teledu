from django.contrib import admin
from teledu.models import CharacterSheet

class CharacterSheetAdmin(admin.ModelAdmin):
  list_display = ['gameSystem', 'name']
  list_display_links = ['name']
  list_filter = ['gameSystem']
  search_fields = ['name']

admin.site.register(CharacterSheet, CharacterSheetAdmin)

