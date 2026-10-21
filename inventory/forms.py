
from django import forms

from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "e.g. Electronics",
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Optional category description",
            }),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "sku",
            "category",
            "description",
            "cost_price",
            "selling_price",
            "stock_quantity",
            "reorder_level",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Product name",
            }),
            "sku": forms.TextInput(attrs={
                "placeholder": "Unique SKU",
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Optional product description",
            }),
            "cost_price": forms.NumberInput(attrs={
                "step": "0.01",
                "min": "0",
            }),
            "selling_price": forms.NumberInput(attrs={
                "step": "0.01",
                "min": "0",
            }),
            "stock_quantity": forms.NumberInput(attrs={
                "min": "0",
            }),
            "reorder_level": forms.NumberInput(attrs={
                "min": "0",
            }),
        }
