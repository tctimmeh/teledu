# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('teledu_characterattributevalue', 'definition_id', 'attribute_id')
        db.rename_column('teledu_conceptattributevalue', 'definition_id', 'attribute_id')

    def backwards(self, orm):
        db.rename_column('teledu_conceptattributevalue', 'attribute_id', 'definition_id')
        db.rename_column('teledu_characterattributevalue', 'attribute_id', 'definition_id')

    models = {
        'teledu.character': {
            'Meta': {'object_name': 'Character'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['teledu.CharacterAttribute']", 'through': "orm['teledu.CharacterAttributeValue']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'teledu.characterattribute': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'CharacterAttribute'},
            'calcFunction': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'dataType': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['teledu.DataType']"}),
            'default': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'characterAttributes'", 'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'valueConcept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.Concept']", 'null': 'True', 'blank': 'True'})
        },
        'teledu.characterattributedependency': {
            'Meta': {'unique_together': "(('attribute', 'dependency'),)", 'object_name': 'CharacterAttributeDependency'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dependencies'", 'to': "orm['teledu.CharacterAttribute']"}),
            'dependency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dependents'", 'to': "orm['teledu.CharacterAttribute']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'teledu.characterattributevalue': {
            'Meta': {'object_name': 'CharacterAttributeValue'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.CharacterAttribute']"}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_value': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'teledu.charactersheet': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'CharacterSheet'},
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'teledu.concept': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'Concept'},
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'teledu.conceptattribute': {
            'Meta': {'unique_together': "(('concept', 'name'),)", 'object_name': 'ConceptAttribute'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributes'", 'to': "orm['teledu.Concept']"}),
            'dataType': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['teledu.DataType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'valueConcept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.Concept']", 'null': 'True', 'blank': 'True'})
        },
        'teledu.conceptattributevalue': {
            'Meta': {'unique_together': "(('attribute', 'instance'),)", 'object_name': 'ConceptAttributeValue'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.ConceptAttribute']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.ConceptInstance']"}),
            'raw_value': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'teledu.conceptinstance': {
            'Meta': {'unique_together': "(('concept', 'name'),)", 'object_name': 'ConceptInstance'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['teledu.ConceptAttribute']", 'through': "orm['teledu.ConceptAttributeValue']", 'symmetrical': 'False'}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.Concept']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
        }
    }

    complete_apps = ['teledu']