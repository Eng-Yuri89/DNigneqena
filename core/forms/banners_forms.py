from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms
from django.forms import BaseFormSet, inlineformset_factory, formset_factory
from djangoformsetjs.utils import formset_media_js

from core.extra.custom_layout_object import *
from core.models.banners import Banners, BannerGroup



class BannerAddForm(forms.ModelForm):
    class Meta:
        model = Banners
        exclude = ()


BannersFormSet = inlineformset_factory(BannerGroup, Banners,
                                            form=BannerAddForm, extra=1)



class BannersGroupForm(forms.ModelForm):

    banner_name=forms.CharField()
    status = forms.ChoiceField(label="status", choices=(
        ('True', 'Enable'),
        ('False', 'Disable'),
    ))






