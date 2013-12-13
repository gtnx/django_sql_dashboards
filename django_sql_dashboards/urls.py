from django.conf.urls import patterns, include, url
from django_sql_dashboards.settings import SQL_DASHBOARDS_MEDIA_ROOT

urlpatterns = patterns('',
  url(r'^$', 'django_sql_dashboards.views.home', name='home'),
  url(r'^query/?$', 'django_sql_dashboards.views.query_all', name='query_all'),
  url(r'^query/add/?$', 'django_sql_dashboards.views.query_editor', name='query_editor'),
  url(r'^query/edit/(\d+)$', 'django_sql_dashboards.views.query_editor', name='query_editor'),

  url(r'^dashboard/?$', 'django_sql_dashboards.views.dashboard_all', name='dashboard_all'),
  url(r'^dashboard/add/?$', 'django_sql_dashboards.views.dashboard_editor', name='dashboard_editor'),
  url(r'^dashboard/edit/(\d+)$', 'django_sql_dashboards.views.dashboard_editor', name='dashboard_editor'),
  url(r'^dashboard/(\d+)/change_order$', 'django_sql_dashboards.views.dashboard_editor_change_order', name='dashboard_editor_change_order'),

  url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                  'document_root': SQL_DASHBOARDS_MEDIA_ROOT}),

  url(r'^test_query$', 'django_sql_dashboards.views.test_query', name='test_query'),

  url(r'.*', 'django_sql_dashboards.views.default', name='default'),
)