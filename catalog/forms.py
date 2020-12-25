from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, Textarea

from catalog.models import Category, Product


class CategoryAddForm(forms.ModelForm):
    title = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),

            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }