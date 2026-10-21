from decimal import Decimal

from django.contrib import messages
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Sum
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, ProductForm
from .models import Category, Product


def _dashboard_context(request, **extra_context):
    active_products = Product.objects.filter(is_active=True)
    query = request.GET.get("q", "").strip()
    category_query = request.GET.get("category_q", "").strip()
    products = Product.objects.select_related("category")
    categories = Category.objects.annotate(products_count=Count("products"))

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(sku__icontains=query)
            | Q(category__name__icontains=query)
        )

    if category_query:
        categories = categories.filter(
            Q(name__icontains=category_query)
            | Q(description__icontains=category_query)
        )

    inventory_value = active_products.aggregate(
        total=Sum(
            ExpressionWrapper(
                F("cost_price") * F("stock_quantity"),
                output_field=DecimalField(max_digits=20, decimal_places=2),
            )
        )
    )["total"] or Decimal("0.00")

    context = {
        "products": products,
        "categories": categories,
        "query": query,
        "category_query": category_query,
        "total_products": active_products.count(),
        "total_categories": Category.objects.count(),
        "low_stock_count": active_products.filter(
            stock_quantity__lte=F("reorder_level")
        ).count(),
        "total_units": active_products.aggregate(
            total=Sum("stock_quantity")
        )["total"] or 0,
        "inventory_value": inventory_value,
        "low_stock_products": (
            active_products.filter(stock_quantity__lte=F("reorder_level"))
            .select_related("category")
            .order_by("stock_quantity")[:10]
        ),
        "product_form": ProductForm(),
        "category_form": CategoryForm(),
        "active_modal": "",
        "editing_product": None,
        "editing_category": None,
    }
    context.update(extra_context)
    return context


def _render_dashboard(request, **extra_context):
    return render(
        request,
        "inventory/dashboard.html",
        _dashboard_context(request, **extra_context),
    )


def dashboard(request):
    return _render_dashboard(request)


def product_list(request):
    return _render_dashboard(request)


def product_create(request):
    form = ProductForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product created successfully.")
        return redirect("inventory:dashboard")

    return _render_dashboard(
        request,
        product_form=form,
        active_modal="product",
    )


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
        return redirect("inventory:dashboard")

    return _render_dashboard(
        request,
        product_form=form,
        active_modal="product",
        editing_product=product,
    )


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")

    return redirect("inventory:dashboard")


def category_list(request):
    return _render_dashboard(request)


def category_create(request):
    form = CategoryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category created successfully.")
        return redirect("inventory:dashboard")

    return _render_dashboard(
        request,
        category_form=form,
        active_modal="category",
    )


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully.")
        return redirect("inventory:dashboard")

    return _render_dashboard(
        request,
        category_form=form,
        active_modal="category",
        editing_category=category,
    )


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        try:
            category.delete()
        except ProtectedError:
            messages.error(
                request,
                "This category still has products assigned to it. "
                "Move or remove those products before deleting the category.",
            )
        else:
            messages.success(request, "Category deleted successfully.")

    return redirect("inventory:dashboard")
