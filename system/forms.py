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

User = get_user_model()

from django.urls import reverse_lazy


class StoreAddForm(forms.ModelForm):

    class Meta:
        model = Store
        fields = '__all__'