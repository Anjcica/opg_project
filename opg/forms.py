from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Opg, Product


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]


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
