# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'CharacterAttribute', fields ['definition', 'character']
        db.create_unique('teledu_characterattribute', ['definition_id', 'character_id'])

        # Adding unique constraint on 'GameSystem', fields ['name']
        db.create_unique('teledu_gamesystem', ['name'])

        # Adding unique constraint on 'CharacterSheet', fields ['gameSystem', 'name']
        db.create_unique('teledu_charactersheet', ['gameSystem_id', 'name'])

        # Adding unique constraint on 'CharacterAttributeDefinition', fields ['gameSystem', 'name']
        db.create_unique('teledu_characterattributedefinition', ['gameSystem_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'CharacterAttributeDefinition', fields ['gameSystem', 'name']
        db.delete_unique('teledu_characterattributedefinition', ['gameSystem_id', 'name'])

        # Removing unique constraint on 'CharacterSheet', fields ['gameSystem', 'name']
        db.delete_unique('teledu_charactersheet', ['gameSystem_id', 'name'])

        # Removing unique constraint on 'GameSystem', fields ['name']
        db.delete_unique('teledu_gamesystem', ['name'])

        # Removing unique constraint on 'CharacterAttribute', fields ['definition', 'character']
        db.delete_unique('teledu_characterattribute', ['definition_id', 'character_id'])


    models = {
        'teledu.character': {
            'Meta': {'object_name': 'Character'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['teledu.CharacterAttributeDefinition']", 'through': "orm['teledu.CharacterAttribute']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'teledu.characterattribute': {
            'Meta': {'unique_together': "(('character', 'definition'),)", 'object_name': 'CharacterAttribute'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.Character']"}),
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.CharacterAttributeDefinition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'teledu.characterattributedefinition': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'CharacterAttributeDefinition'},
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'teledu.charactersheet': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'CharacterSheet'},
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'teledu.gamesystem': {
            'Meta': {'object_name': 'GameSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['teledu']