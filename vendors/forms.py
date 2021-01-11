from django import forms
from django.contrib import messages
from django.shortcuts import render
from requests import request

from accounts.forms import UserRegisterForm
from accounts.models import User
from vendors.models import Store


class StoreAddForm(forms.ModelForm):
    class Meta:
        model = Store
        # fields = '__all__'
        fields = ['email', 'phone']
        exclude = ['vendor']

        def clean_title(self, title):
            from django.utils.text import slugify
            from django.core.exceptions import ValidationError

            email = slugify(title)
            if Store.objects.filter(email=email).exists():
                raise ValidationError('Store with this Email already exists.')


class StoreAddFormm(forms.ModelForm):
    class Meta:
        model = Store

        # fields = '__all__'
        fields = ['email', 'phone', 'vendor']

        # exclude=['vendor']

    # exclude = ('vendor',)  # ETA: added comma to make this a tuple
    def user(self):

        user = User.objects.filter(pk=id)
        if user is None:
            messages.error(
                request, 'Account is not active,please check your email')
            return render(request, 'front/UsersAccount/CustomerRegister.html', context={
                "title": "Register",
                "form": UserRegisterForm
            })
        else:
            def save(self, commit=True):
                obj = super(StoreAddForm, self).save(False)
                # obj.vendor = User.objects.filter(vendor=)
                commit and obj.save()
                return obj


class StoreEditForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'
