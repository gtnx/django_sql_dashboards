# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

from django.conf import settings


def prefix(request):
    return {
        'SQL_DASHBOARDS_PREFIX': settings.SQL_DASHBOARDS_PREFIX
    }
