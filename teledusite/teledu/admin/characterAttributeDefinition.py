from django.contrib import admin
from teledu.models import CharacterAttributeDependency, CharacterAttributeDefinition

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

admin.site.register(CharacterAttributeDefinition, CharacterAttributeDefinitionAdmin)

