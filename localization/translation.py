from modeltranslation.translator import (
    translator,
    register,
    TranslationOptions,
)

from localization.models import Home


class HomeTranslationsOptions(TranslationOptions):
    fields = ('title', 'content', 'slug')
    empty_values = {'slug': None}


translator.register(Home, HomeTranslationsOptions)