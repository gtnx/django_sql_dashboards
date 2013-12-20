from models import Query, Dashboard, DbConfig
import django_filters

class QueryFilter(django_filters.FilterSet):
  db = django_filters.ModelChoiceFilter(queryset = DbConfig.objects.all(), widget = django_filters.widgets.LinkWidget)
  class Meta:
    model = Query
    fields = ['db']

class DashboardFilter(django_filters.FilterSet):
  # db = django_filters.ModelChoiceFilter(queryset = DbConfig.objects.all(), widget = django_filters.widgets.LinkWidget)
  class Meta:
    model = Dashboard
    fields = []