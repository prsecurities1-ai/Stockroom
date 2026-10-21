from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class InventoryDashboardTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Desk Lamp",
            sku="LAMP-001",
            cost_price="12.50",
            selling_price="20.00",
            stock_quantity=4,
            reorder_level=5,
        )

    def test_dashboard_lists_products_categories_and_stock_metrics(self):
        response = self.client.get(reverse("inventory:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/dashboard.html")
        self.assertContains(response, "Desk Lamp")
        self.assertContains(response, "Electronics")
        self.assertEqual(response.context["total_products"], 1)
        self.assertEqual(response.context["low_stock_count"], 1)
        self.assertEqual(response.context["total_units"], 4)
        self.assertContains(response, "₹50.00")

    def test_product_create_edit_and_delete(self):
        create_response = self.client.post(
            reverse("inventory:product_create"),
            {
                "category": self.category.pk,
                "name": "Keyboard",
                "sku": "KEY-001",
                "cost_price": "25.00",
                "selling_price": "40.00",
                "stock_quantity": "12",
                "reorder_level": "3",
                "description": "Mechanical keyboard",
                "is_active": "on",
            },
        )

        self.assertRedirects(create_response, reverse("inventory:dashboard"))
        keyboard = Product.objects.get(sku="KEY-001")
        edit_response = self.client.post(
            reverse("inventory:product_edit", args=[keyboard.pk]),
            {
                "category": self.category.pk,
                "name": "Keyboard Pro",
                "sku": "KEY-001",
                "cost_price": "30.00",
                "selling_price": "50.00",
                "stock_quantity": "15",
                "reorder_level": "4",
                "description": "",
                "is_active": "on",
            },
        )

        self.assertRedirects(edit_response, reverse("inventory:dashboard"))
        keyboard.refresh_from_db()
        self.assertEqual(keyboard.name, "Keyboard Pro")
        self.assertEqual(keyboard.stock_quantity, 15)

        delete_response = self.client.post(
            reverse("inventory:product_delete", args=[keyboard.pk])
        )

        self.assertRedirects(delete_response, reverse("inventory:dashboard"))
        self.assertFalse(Product.objects.filter(pk=keyboard.pk).exists())

    def test_category_create_edit_and_delete(self):
        create_response = self.client.post(
            reverse("inventory:category_create"),
            {"name": "Office", "description": "Office supplies"},
        )

        self.assertRedirects(create_response, reverse("inventory:dashboard"))
        category = Category.objects.get(name="Office")
        edit_response = self.client.post(
            reverse("inventory:category_edit", args=[category.pk]),
            {"name": "Office supplies", "description": "Updated description"},
        )

        self.assertRedirects(edit_response, reverse("inventory:dashboard"))
        category.refresh_from_db()
        self.assertEqual(category.name, "Office supplies")

        delete_response = self.client.post(
            reverse("inventory:category_delete", args=[category.pk])
        )

        self.assertRedirects(delete_response, reverse("inventory:dashboard"))
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())

    def test_category_with_products_cannot_be_deleted(self):
        response = self.client.post(
            reverse("inventory:category_delete", args=[self.category.pk])
        )

        self.assertRedirects(response, reverse("inventory:dashboard"))
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())
        self.assertContains(
            self.client.get(reverse("inventory:dashboard")),
            "Move or remove those products before deleting the category.",
        )

    def test_invalid_product_submission_reopens_form_with_errors(self):
        response = self.client.post(
            reverse("inventory:product_create"),
            {
                "category": self.category.pk,
                "name": "Broken SKU",
                "sku": self.product.sku,
                "cost_price": "1.00",
                "selling_price": "2.00",
                "stock_quantity": "1",
                "reorder_level": "0",
                "description": "",
                "is_active": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["active_modal"], "product")
        self.assertContains(response, "Product with this Sku already exists.")
        self.assertFalse(Product.objects.filter(name="Broken SKU").exists())
