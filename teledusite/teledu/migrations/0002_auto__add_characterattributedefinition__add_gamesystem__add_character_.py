# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CharacterAttributeDefinition'
        db.create_table('teledu_characterattributedefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gameSystem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teledu.GameSystem'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('teledu', ['CharacterAttributeDefinition'])

        # Adding model 'GameSystem'
        db.create_table('teledu_gamesystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('teledu', ['GameSystem'])

        # Adding model 'Character'
        db.create_table('teledu_character', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('teledu', ['Character'])

        # Adding model 'CharacterAttribute'
        db.create_table('teledu_characterattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teledu.Character'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teledu.CharacterAttributeDefinition'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('teledu', ['CharacterAttribute'])


    def backwards(self, orm):
        # Deleting model 'CharacterAttributeDefinition'
        db.delete_table('teledu_characterattributedefinition')

        # Deleting model 'GameSystem'
        db.delete_table('teledu_gamesystem')

        # Deleting model 'Character'
        db.delete_table('teledu_character')

        # Deleting model 'CharacterAttribute'
        db.delete_table('teledu_characterattribute')


    models = {
        'teledu.character': {
            'Meta': {'object_name': 'Character'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['teledu.CharacterAttributeDefinition']", 'through': "orm['teledu.CharacterAttribute']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'teledu.characterattribute': {
            'Meta': {'object_name': 'CharacterAttribute'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.CharacterAttributeDefinition']"}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'teledu.characterattributedefinition': {
            'Meta': {'object_name': 'CharacterAttributeDefinition'},
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'teledu.gamesystem': {
            'Meta': {'object_name': 'GameSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['teledu']