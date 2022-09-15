from django.forms import ModelForm
from .models import Opg, Product


class OpgForm (ModelForm):
    class Meta:
        model = Opg
        fields = [
            'name',
            'address',
            'phone'
        ]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category']
