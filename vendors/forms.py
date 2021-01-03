from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from system.models import Store
from vendors.models import Vendor

User = get_user_model()

from django.urls import reverse_lazy


class VendorAddForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = '__all__'