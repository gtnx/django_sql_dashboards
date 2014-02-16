from django.conf import settings 

def prefix(request):
  return {'SQL_DASHBOARDS_PREFIX': settings.SQL_DASHBOARDS_PREFIX}