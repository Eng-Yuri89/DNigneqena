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

from catalog.models.models import Category, Product, Images
from catalog.models.product_options import Manufacturer, SingleProduct


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
class CustomUploadFile(Field):
    template = 'add-product.html'


class CustomFieldForm(ProductAddForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('image', css_class='fa fa-plus'),

                css_class='form-row'
            ),

            Submit('image'),  # <-- Here

        )



class ImageForm(forms.ModelForm):
    image = ImageField(label='image')

    class Meta:
        model = Images
        fields = ['image', ]


class ManufacturerAddForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'
