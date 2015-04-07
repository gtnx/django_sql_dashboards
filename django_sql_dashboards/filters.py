# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import django_filters
from django.contrib.auth.models import User

from .models import Query, Dashboard, DbConfig


class QueryFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_type="icontains")
    db = django_filters.ModelChoiceFilter(queryset=DbConfig.objects.exclude(query=None), widget=django_filters.widgets.LinkWidget)
    creator = django_filters.ModelChoiceFilter(queryset=User.objects.exclude(query=None), widget=django_filters.widgets.LinkWidget)

    class Meta:
        model = Query
        fields = ('title', 'creator', 'db')


class DashboardFilter(django_filters.FilterSet):
    creator = django_filters.ModelChoiceFilter(queryset=User.objects.exclude(query=None), widget=django_filters.widgets.LinkWidget)

    class Meta:
        model = Dashboard
        fields = ('creator',)
