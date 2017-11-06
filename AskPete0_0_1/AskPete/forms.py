from django import forms
from django.http import HttpResponse, HttpResponseRedirect

class SearchForm(forms.Form):

    query = forms.CharField(label='query', max_length=400)
    print(query)