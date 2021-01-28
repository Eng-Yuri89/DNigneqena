from django import forms

from sales.models.order import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'