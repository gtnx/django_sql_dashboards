from django import forms
from models import Query, Dashboard

class QueryForm(forms.ModelForm):
  class Meta:
    model = Query
    widgets = {'query': forms.Textarea(attrs={'cols': 90, 'rows': 4}),}
    exclude = ["creator"]

  def save(self, user, *args, **kwargs):
    inst = super(QueryForm, self).save(commit = False)
    inst.creator = user
    if kwargs.get("commit", False):
      inst.save()
    return inst

class QueryAddForm(forms.Form):
  query = forms.ModelChoiceField(queryset = Query.objects.all())

class DashboardForm(forms.ModelForm):
  class Meta:
    model = Dashboard
    exclude = ["creator"]

  def save(self, user, *args, **kwargs):
    inst = super(DashboardForm, self).save(commit = False)
    inst.creator = user
    if kwargs.get("commit", False):
      inst.save()
    return inst