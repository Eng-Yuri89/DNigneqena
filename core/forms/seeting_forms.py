from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from core.models.models import Setting
from vendors.models import Store


class SettingAddForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'
