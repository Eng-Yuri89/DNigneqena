from modeltranslation.translator import translator, TranslationOptions

from catalog.models.models import Category


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'slug')


translator.register(Category, CategoryTranslationOptions)
