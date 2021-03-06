# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ConceptInstance'
        db.create_table('teledu_conceptinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('teledu', ['ConceptInstance'])

        # Adding model 'GameSystemConcept'
        db.create_table('teledu_gamesystemconcept', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gameSystem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teledu.GameSystem'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('teledu', ['GameSystemConcept'])

        # Adding unique constraint on 'GameSystemConcept', fields ['gameSystem', 'name']
        db.create_unique('teledu_gamesystemconcept', ['gameSystem_id', 'name'])

        # Adding model 'ConceptInstanceAttribute'
        db.create_table('teledu_conceptinstanceattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teledu.ConceptAttributeDefinition'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teledu.ConceptInstance'])),
            ('raw_value', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('teledu', ['ConceptInstanceAttribute'])

        # Adding unique constraint on 'ConceptInstanceAttribute', fields ['definition', 'instance']
        db.create_unique('teledu_conceptinstanceattribute', ['definition_id', 'instance_id'])

        # Adding model 'ConceptAttributeDefinition'
        db.create_table('teledu_conceptattributedefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teledu.GameSystemConcept'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('dataType', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['teledu.DataType'])),
        ))
        db.send_create_signal('teledu', ['ConceptAttributeDefinition'])

        # Adding unique constraint on 'ConceptAttributeDefinition', fields ['concept', 'name']
        db.create_unique('teledu_conceptattributedefinition', ['concept_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'ConceptAttributeDefinition', fields ['concept', 'name']
        db.delete_unique('teledu_conceptattributedefinition', ['concept_id', 'name'])

        # Removing unique constraint on 'ConceptInstanceAttribute', fields ['definition', 'instance']
        db.delete_unique('teledu_conceptinstanceattribute', ['definition_id', 'instance_id'])

        # Removing unique constraint on 'GameSystemConcept', fields ['gameSystem', 'name']
        db.delete_unique('teledu_gamesystemconcept', ['gameSystem_id', 'name'])

        # Deleting model 'ConceptInstance'
        db.delete_table('teledu_conceptinstance')

        # Deleting model 'GameSystemConcept'
        db.delete_table('teledu_gamesystemconcept')

        # Deleting model 'ConceptInstanceAttribute'
        db.delete_table('teledu_conceptinstanceattribute')

        # Deleting model 'ConceptAttributeDefinition'
        db.delete_table('teledu_conceptattributedefinition')


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
            'raw_value': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'teledu.characterattributedefinition': {
            'Meta': {'unique_together': "(('gameSystem', 'name'),)", 'object_name': 'CharacterAttributeDefinition'},
            'calcFunction': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'dataType': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['teledu.DataType']"}),
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
        'teledu.conceptattributedefinition': {
            'Meta': {'unique_together': "(('concept', 'name'),)", 'object_name': 'ConceptAttributeDefinition'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystemConcept']"}),
            'dataType': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['teledu.DataType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'teledu.conceptinstance': {
            'Meta': {'object_name': 'ConceptInstance'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['teledu.ConceptAttributeDefinition']", 'through': "orm['teledu.ConceptInstanceAttribute']", 'symmetrical': 'False'}),
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