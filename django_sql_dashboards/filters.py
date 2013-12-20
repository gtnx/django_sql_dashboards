from django.contrib.auth.models import User
from models import Query, Dashboard, DbConfig
import django_filters

class QueryFilter(django_filters.FilterSet):
  db = django_filters.ModelChoiceFilter(queryset = DbConfig.objects.exclude(query = None), widget = django_filters.widgets.LinkWidget)
  creator = django_filters.ModelChoiceFilter(queryset = User.objects.exclude(query = None), widget = django_filters.widgets.LinkWidget)
  class Meta:
    model = Query
    fields = ['creator', 'db']

class DashboardFilter(django_filters.FilterSet):
  # db = django_filters.ModelChoiceFilter(queryset = DbConfig.objects.all(), widget = django_filters.widgets.LinkWidget)
  class Meta:
    model = Dashboard
    fields = []