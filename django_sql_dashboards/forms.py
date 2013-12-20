from django import forms
from models import Query

class QueryForm(forms.ModelForm):
  class Meta:
    model = Query
    widgets = {'query': forms.Textarea(attrs={'cols': 90, 'rows': 4}),}

class QueryAddForm(forms.Form):
  query = forms.ModelChoiceField(queryset = Query.objects.all())