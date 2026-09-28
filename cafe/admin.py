from django.contrib import admin

from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "is_available",
        "created_at",
    )

    list_filter = (
        "category",
        "is_available",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_editable = (
        "price",
        "is_available",
    )


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    fields = (
        "product",
        "quantity",
        "price",
        "item_subtotal",
    )

    readonly_fields = (
        "price",
        "item_subtotal",
    )

    @admin.display(
        description="Subtotal"
    )
    def item_subtotal(self, obj):

        if obj.price is None:
            return "₹0.00"

        return f"₹{obj.price * obj.quantity:.2f}"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "table_name",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
        "table_name",
    )

    search_fields = (
        "table_name",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "total_amount",
        "created_at",
    )

    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "quantity",
        "price",
        "item_subtotal",
    )

    search_fields = (
        "product__name",
        "order__table_name",
    )

    @admin.display(
        description="Subtotal"
    )
    def item_subtotal(self, obj):

        if obj.price is None:
            return "₹0.00"  

        return f"₹{obj.price * obj.quantity:.2f}"