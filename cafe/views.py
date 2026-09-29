from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from django.db.models import Q

from .models import Product, Order, OrderItem
from .forms import CheckoutForm


def home(request):

    # Get all available products
    products = Product.objects.filter(
        is_available=True
    ).order_by("name")

    # Get cart from session
    cart = request.session.get(
        "cart",
        {}
    )

    # Calculate total items in cart
    cart_count = sum(
        cart.values()
    )

    return render(
        request,
        "cafe/home.html",
        {
            "products": products,
            "cart_count": cart_count,
        }
    )
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    cart = request.session.get("cart", {})

    product_id_str = str(product.id)

    # Add/increase quantity
    cart[product_id_str] = cart.get(product_id_str, 0) + 1

    request.session["cart"] = cart
    request.session.modified = True

    # Calculate total cart quantity
    cart_count = sum(cart.values())

    # AJAX request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return JsonResponse({
            "success": True,
            "message": f"{product.name} added to cart",
            "product_name": product.name,
            "cart_count": cart_count,
        })

    # Normal request fallback
    messages.success(
        request,
        f"{product.name} added to cart."
    )

    return redirect("home")

def cart(request):

    cart_data = request.session.get("cart", {})

    cart_items = []
    total = Decimal("0")

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    return render(
        request,
        "cafe/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
            "cart_count": sum(cart_data.values()),
        }
    )


def increase_cart(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def decrease_cart(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def checkout(request):

    cart_data = request.session.get("cart", {})

    if not cart_data:
        messages.warning(
            request,
            "Your cart is empty."
        )
        return redirect("home")

    total = Decimal("0")

    cart_items = []

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            table_name = form.cleaned_data["table_name"]

            # Create order
            order = Order.objects.create(
                table_name=table_name,
                total_amount=total,
                status="Pending"
            )

            # Add products to order
            for item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price
                )

            # Clear cart
            request.session["cart"] = {}
            request.session.modified = True

            return render(
                request,
                "cafe/order_success.html",
                {
                    "order": order,
                }
            )

    else:

        form = CheckoutForm()

    return render(
        request,
        "cafe/checkout.html",
        {
            "form": form,
            "cart_items": cart_items,
            "total": total,
            "cart_count": sum(cart_data.values()),
        }
    )