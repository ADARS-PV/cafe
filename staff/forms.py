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
            "category",
            "description",
            "price",
            "image",
            "is_available",
            "stock",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Product name"
                }
            ),

            "category": forms.Select(),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Product description",
                    "rows": 4,
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "placeholder": "0.00",
                    "step": "0.01",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "placeholder": "Available quantity"
                }
            ),

            "image": forms.ClearableFileInput(),

            "is_available": forms.CheckboxInput(),
        }