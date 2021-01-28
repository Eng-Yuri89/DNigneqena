import datetime
from urllib import request

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit
from easy_select2.widgets import Select2
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, Textarea, ImageField
from haystack import indexes

from catalog.models.models import Category, Product, Image
from catalog.models.product_options import Manufacturer, SingleProduct
from core.models.models import Images


class CategoryAddForm(forms.ModelForm):
    title = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Category
        fields = '__all__'


class SingleProductAddForm(forms.ModelForm):
    class Meta:
        model = SingleProduct
        fields = ['title', ]


class ProductAddForm(forms.ModelForm):
    thumbnail = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, label='image')
    status = forms.ChoiceField(label="status", choices=(
        ('True', 'Enable'),
        ('False', 'Disable'),))
    variant = forms.ChoiceField(label="variant",
        choices = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),))





    class Meta:
        model = Product
        fields = '__all__'
        # extra_field = CategoryAddForm.Meta.fields
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'keywords': forms.TextInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'custom-select'}),
                   #'variant': forms.Select(attrs={'class': 'custom-select'}),
                   'slug': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'detail': CKEditorWidget(attrs={'class': 'form-control'}),

                   }


class ImageForm(forms.ModelForm):

    class Meta:
        model = Images
        fields = ('image',)


class ProductFullForm(ProductAddForm):
    product_id = forms.IntegerField(required=False)
    thumbnail = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False )
    image1 = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    tags = forms.CharField(max_length=50, required=False)

    class Meta(ProductAddForm.Meta):
        fields = '__all__'
        field_classes=ProductAddForm.Meta.fields

        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'keywords': forms.TextInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'custom-select'}),
                   #'variant': forms.Select(attrs={'class': 'custom-select'}),
                   'slug': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'detail': CKEditorWidget(attrs={'class': 'form-control'}),

                   }

    def save(self, *args, **kwargs):
        image = super(ProductFullForm, self).save(*args, **kwargs)
        if hasattr(self.files, 'getlist'):
            for f in self.files.getlist('image'):
                Image.objects.create(product=image, image=f)
        return image


class ManufacturerAddForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    category = indexes.CharField(model_attr='catalog')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
