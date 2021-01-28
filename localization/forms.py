from modeltranslation.forms import TranslationModelForm

from locale.models import Home


class MyForm(TranslationModelForm):
    class Meta:
        model = Home