# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup

from .models import Query, Dashboard


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        widgets = {'query': forms.Textarea(attrs={'cols': 90, 'rows': 4})}
        exclude = ("creator",)

    def __init__(self, *args, **kwargs):
        super(QueryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            ButtonHolder(
                Submit('run', 'Run'),
                Submit('save', 'Save'),
                Submit('run_save', 'Run & Save'),
                HTML("""<a href="%s/query/add" class="btn btn-success">+ Add</a>""" % settings.SQL_DASHBOARDS_PREFIX),
            ),
            HTML("<br>"),
            Fieldset('', 'db', 'title', 'type', 'query', 'pivot'),
            Accordion(AccordionGroup('Other options', 'subtitle', 'xlegend', 'ylegend', 'public', 'legend_align', 'cache_ttl')),
            HTML("<br>"),
            ButtonHolder(
                Submit('run', 'Run'),
                Submit('save', 'Save'),
                Submit('run_save', 'Run & Save'),
                HTML("""<a href="%s/query/add" class="btn btn-success">+ Add</a>""" % settings.SQL_DASHBOARDS_PREFIX),
            ),
        )

    def save(self, user, *args, **kwargs):
        inst = super(QueryForm, self).save(commit=False)
        inst.creator = user
        if kwargs.get("commit", False):
            inst.save()
        return inst


class QueryAddForm(forms.Form):
    query = forms.ModelChoiceField(queryset=Query.objects.all())

    def __init__(self, *args, **kwargs):
        super(QueryAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('add', 'Add'))


class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        exclude = ["creator"]

    def __init__(self, *args, **kwargs):
        super(DashboardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('add', 'Create Dashboard'))

    def save(self, user, *args, **kwargs):
        inst = super(DashboardForm, self).save(commit=False)
        inst.creator = user
        if kwargs.get("commit", False):
            inst.save()
        return inst


class CustomQueryForm(forms.Form):
    limit = forms.IntegerField(required=False, initial=10)

    def __init__(self, query, *args, **kwargs):
        super(CustomQueryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        field_set = Fieldset('')
        has_limit = "%(limit)s" in query.query
        if has_limit:
            field_set.fields.append('limit')
        self.helper.layout = Layout(
            field_set,
            ButtonHolder(Submit('run', 'Run')),
        )
