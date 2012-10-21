# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'CharacterAttribute', fields ['definition', 'character']
        db.delete_unique('teledu_characterattribute', ['definition_id', 'character_id'])

        # Adding field 'CharacterAttributeDefinition.list'
        db.add_column('teledu_characterattributedefinition', 'list',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CharacterAttributeDefinition.list'
        db.delete_column('teledu_characterattributedefinition', 'list')

        # Adding unique constraint on 'CharacterAttribute', fields ['definition', 'character']
        db.create_unique('teledu_characterattribute', ['definition_id', 'character_id'])


    models = {
        'teledu.character': {
            'Meta': {'object_name': 'Character'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['teledu.CharacterAttributeDefinition']", 'through': "orm['teledu.CharacterAttribute']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'teledu.characterattribute': {
            'Meta': {'object_name': 'CharacterAttribute'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.Character']"}),
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.CharacterAttributeDefinition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_value': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'teledu.characterattributedefinition': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'CharacterAttributeDefinition'},
            'calcFunction': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystemConcept']", 'null': 'True', 'blank': 'True'}),
            'dataType': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['teledu.DataType']"}),
            'default': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'characterAttributeDefinitions'", 'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'teledu.characterattributedependency': {
            'Meta': {'unique_together': "(('attribute', 'dependency'),)", 'object_name': 'CharacterAttributeDependency'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dependencies'", 'to': "orm['teledu.CharacterAttributeDefinition']"}),
            'dependency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dependents'", 'to': "orm['teledu.CharacterAttributeDefinition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'teledu.charactersheet': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'CharacterSheet'},
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'teledu.conceptattributedefinition': {
            'Meta': {'unique_together': "(('concept', 'name'),)", 'object_name': 'ConceptAttributeDefinition'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributeDefinitions'", 'to': "orm['teledu.GameSystemConcept']"}),
            'dataType': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['teledu.DataType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'teledu.conceptinstance': {
            'Meta': {'unique_together': "(('concept', 'name'),)", 'object_name': 'ConceptInstance'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['teledu.ConceptAttributeDefinition']", 'through': "orm['teledu.ConceptInstanceAttribute']", 'symmetrical': 'False'}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystemConcept']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'teledu.conceptinstanceattribute': {
            'Meta': {'unique_together': "(('definition', 'instance'),)", 'object_name': 'ConceptInstanceAttribute'},
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.ConceptAttributeDefinition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.ConceptInstance']"}),
            'raw_value': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'teledu.datatype': {
            'Meta': {'object_name': 'DataType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        },
        'teledu.gamesystem': {
            'Meta': {'object_name': 'GameSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'teledu.gamesystemconcept': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'GameSystemConcept'},
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['teledu']