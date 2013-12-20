# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DbConfig'
        db.create_table(u'django_sql_dashboards_dbconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('passwd', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('db', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ts_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ts_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'django_sql_dashboards', ['DbConfig'])

        # Adding model 'Query'
        db.create_table(u'django_sql_dashboards_query', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_sql_dashboards.DbConfig'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('xlegend', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('ylegend', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('query', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ts_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ts_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'django_sql_dashboards', ['Query'])

        # Adding model 'Dashboard'
        db.create_table(u'django_sql_dashboards_dashboard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('column_nb', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'django_sql_dashboards', ['Dashboard'])

        # Adding model 'DashboardQuery'
        db.create_table(u'django_sql_dashboards_dashboardquery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dashboard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_sql_dashboards.Dashboard'])),
            ('query', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_sql_dashboards.Query'])),
            ('order_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'django_sql_dashboards', ['DashboardQuery'])

        # Adding unique constraint on 'DashboardQuery', fields ['dashboard', 'query']
        db.create_unique(u'django_sql_dashboards_dashboardquery', ['dashboard_id', 'query_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'DashboardQuery', fields ['dashboard', 'query']
        db.delete_unique(u'django_sql_dashboards_dashboardquery', ['dashboard_id', 'query_id'])

        # Deleting model 'DbConfig'
        db.delete_table(u'django_sql_dashboards_dbconfig')

        # Deleting model 'Query'
        db.delete_table(u'django_sql_dashboards_query')

        # Deleting model 'Dashboard'
        db.delete_table(u'django_sql_dashboards_dashboard')

        # Deleting model 'DashboardQuery'
        db.delete_table(u'django_sql_dashboards_dashboardquery')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ts_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ts_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'django_sql_dashboards.query': {
            'Meta': {'object_name': 'Query'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_sql_dashboards.DbConfig']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ts_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ts_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'xlegend': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ylegend': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['django_sql_dashboards']