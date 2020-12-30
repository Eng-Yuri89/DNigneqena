from urllib import request
from easy_select2.widgets import Select2
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, Textarea

from catalog.models import Category, Product, ImageAlbum, Manufacturer


class CategoryAddForm(forms.ModelForm):
    title = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Category
        fields = '__all__'


class ProductAddForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(ProductAddForm, self).__init__(*args, **kargs)


    status= forms.ChoiceField(label="status", choices=(
        ('True', 'Enable'),
        ('False', 'Disable'),
    ))
    class Meta:
        model = Product
        fields = '__all__'
        extra_field = CategoryAddForm.Meta.fields
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'keywords': forms.TextInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'form-control'}),
                   'slug': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),

                   }


class ProductFullForm(ProductAddForm):
    def __init__(self, *args, **kargs):
        super(ProductFullForm, self).__init__(*args, **kargs)
    product_id = forms.IntegerField(required=False)
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    tags = forms.CharField(max_length=50, required=False)

    class Meta(ProductAddForm.Meta):
        fields = ['images', 'tags', 'product_id']
        extra_field = ProductAddForm.Meta.fields


class ManufacturerAddForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'
