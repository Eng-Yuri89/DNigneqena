from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms
from django.forms import BaseFormSet, inlineformset_factory, formset_factory, modelformset_factory
from djangoformsetjs.utils import formset_media_js

from core.extra.custom_layout_object import *
from core.models.banners import Banners


class BannerAddForm(forms.ModelForm):
    class Meta:
        model = Banners

        exclude = ['image','link','sort_order','caption']


#BannersFormSet = modelformset_factory(Banners, form=BannerAddForm,exclude=['group','status'], extra=1,can_delete=True)


