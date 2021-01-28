from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from core.models.models import Setting, SettingLang
from vendors.models import Store


class SettingAddForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'


class SettingLangAddForm(SettingAddForm):
    class Meta:
        model = SettingLang
        fields = '__all__'
        exclude=('setting',)
