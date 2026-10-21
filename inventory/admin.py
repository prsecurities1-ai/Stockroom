
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "cost_price",
        "selling_price",
        "stock_quantity",
        "reorder_level",
        "is_low_stock",
        "is_active",
    )
    list_filter = ("category", "is_active")
    search_fields = ("name", "sku")
    list_select_related = ("category",)
    ordering = ("name",)
    list_editable = ("stock_quantity", "is_active")
    readonly_fields = ("created_at", "updated_at")
