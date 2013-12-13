# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Dashboard.column_nb'
        db.add_column(u'sql_dashboard', 'column_nb',
                      self.gf('django.db.models.fields.IntegerField')(default=3),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Dashboard.column_nb'
        db.delete_column(u'sql_dashboard', 'column_nb')


    models = {
        u'sql.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            'column_nb': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sql.Query']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'sql.dbconfig': {
            'Meta': {'object_name': 'DbConfig'},
            'db': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ts_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ts_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sql.query': {
            'Meta': {'object_name': 'Query'},
            'db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sql.DbConfig']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'xlegend': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ylegend': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['sql']