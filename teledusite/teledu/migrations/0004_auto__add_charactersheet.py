# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CharacterSheet'
        db.create_table('teledu_charactersheet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gameSystem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teledu.GameSystem'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('template', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('teledu', ['CharacterSheet'])


    def backwards(self, orm):
        # Deleting model 'CharacterSheet'
        db.delete_table('teledu_charactersheet')


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
            'value': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'teledu.characterattributedefinition': {
            'Meta': {'object_name': 'CharacterAttributeDefinition'},
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'teledu.charactersheet': {
            'Meta': {'object_name': 'CharacterSheet'},
            'gameSystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teledu.GameSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.TextField', [], {})
        },
        'teledu.gamesystem': {
            'Meta': {'object_name': 'GameSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['teledu']