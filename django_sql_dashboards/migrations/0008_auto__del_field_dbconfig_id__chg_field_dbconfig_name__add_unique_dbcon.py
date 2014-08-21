# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DbConfig.id'
        db.delete_column(u'django_sql_dashboards_dbconfig', u'id')


        # Changing field 'DbConfig.name'
        db.alter_column(u'django_sql_dashboards_dbconfig', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True))
        # Adding unique constraint on 'DbConfig', fields ['name']
        db.create_unique(u'django_sql_dashboards_dbconfig', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'DbConfig', fields ['name']
        db.delete_unique(u'django_sql_dashboards_dbconfig', ['name'])


        # User chose to not deal with backwards NULL issues for 'DbConfig.id'
        raise RuntimeError("Cannot reverse this migration. 'DbConfig.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'DbConfig.id'
        db.add_column(u'django_sql_dashboards_dbconfig', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)


        # Changing field 'DbConfig.name'
        db.alter_column(u'django_sql_dashboards_dbconfig', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_sql_dashboards.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            'column_nb': ('django.db.models.fields.IntegerField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'django_sql_dashboards.dashboardquery': {
            'Meta': {'unique_together': "(['dashboard', 'query'],)", 'object_name': 'DashboardQuery'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_sql_dashboards.Dashboard']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {}),
            'query': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_sql_dashboards.Query']"})
        },
        u'django_sql_dashboards.dbconfig': {
            'Meta': {'ordering': "['name']", 'object_name': 'DbConfig'},
            'db': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ts_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ts_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'django_sql_dashboards.query': {
            'Meta': {'object_name': 'Query'},
            'cache_ttl': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'custom': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_sql_dashboards.DbConfig']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legend_align': ('django.db.models.fields.CharField', [], {'default': "'right'", 'max_length': '64'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ts_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ts_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'xlegend': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ylegend': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'django_sql_dashboards.queryhistory': {
            'Meta': {'object_name': 'QueryHistory'},
            'data': ('picklefield.fields.PickledObjectField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_sql_dashboards.Query']"}),
            'ts_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ts_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['django_sql_dashboards']