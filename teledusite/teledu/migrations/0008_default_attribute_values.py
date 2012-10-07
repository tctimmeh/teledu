# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CharacterAttributeDefinition.default'
        db.add_column('teledu_characterattributedefinition', 'default',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)


        # Changing field 'CharacterAttribute.value'
        db.alter_column('teledu_characterattribute', 'value', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):
        # Deleting field 'CharacterAttributeDefinition.default'
        db.delete_column('teledu_characterattributedefinition', 'default')


        # Changing field 'CharacterAttribute.value'
        db.alter_column('teledu_characterattribute', 'value', self.gf('django.db.models.fields.TextField')(null=True))

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
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'teledu.characterattributedefinition': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'CharacterAttributeDefinition'},
            'calcFunction': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'teledu.gamesystem': {
            'Meta': {'object_name': 'GameSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['teledu']