from django import forms
from django.contrib.auth import authenticate

from accounts.models import User
from vendors.models import Store


class StoreAddForm(forms.ModelForm):


    class Meta:
        model = Store
        fields = '__all__'


class StoreEditForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'


