from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render
from requests import request

from accounts.forms import UserRegisterForm
from accounts.models import User
from vendors.models import Store


class StoreAddForm(forms.ModelForm):

    class Meta:
        model = Store
        fields = ['email','phone']
        #exclude = ('vendor',)  # ETA: added comma to make this a tuple
    def user(self):
        vendor= Store.objects.get(User_id=id)
        if vendor is None:
            messages.error(
                request, 'Account is not active,please check your email')
            return render(request, 'front/UsersAccount/CustomerRegister.html', context={
                "title": "Register",
                "form": UserRegisterForm
            })
        else:
            def __init__(self, *args, **kwargs):
                self.vendor = kwargs['initial']['vendor']
                super(StoreAddForm, self).__init__(*args, **kwargs)

            def save(self, commit=True):
                obj = super(StoreAddForm, self).save(False)
                obj.vendor = self.vendor
                commit and obj.save()
                return obj




class StoreEditForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'


