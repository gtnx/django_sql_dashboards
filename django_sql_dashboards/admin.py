# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

from django.contrib import admin

from .models import DbConfig, Query, Dashboard


class DbConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "host", "db")
    list_filter = ("host",)
    search_fields = ("name",)
admin.site.register(DbConfig, DbConfigAdmin)


class QueryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Query, QueryAdmin)


class DashboardAdmin(admin.ModelAdmin):
    exclude = ("creator",)
    list_display = ("title", "creator")

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()
admin.site.register(Dashboard, DashboardAdmin)
