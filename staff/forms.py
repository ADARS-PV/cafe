from django import forms
from django.contrib.auth.forms import AuthenticationForm

from cafe.models import Product


class StaffLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Password",
            }
        )
    )


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [
            "name",
            "description",
            "price",
            "image",
            "category",
            "is_available",
        ]