from django import forms
from django.forms import TextInput, FileInput





class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()



