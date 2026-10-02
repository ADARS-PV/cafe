from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import ensure_csrf_cookie


from django.contrib import messages

from django.db.models import Q

from .models import Product, Order, OrderItem
from .forms import CheckoutForm


@ensure_csrf_cookie
def home(request):

    search_query = request.GET.get(
        "q",
        ""
    ).strip()

    category = request.GET.get(
        "category",
        ""
    ).upper()


    products = Product.objects.filter(
        is_available=True
    )


    if search_query:

        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )


    if category in [
        "HOT",
        "COOL",
        "SNACKS"
    ]:

        products = products.filter(
            category=category
        )


    cart = request.session.get(
        "cart",
        {}
    )


    cart_count = sum(
        int(quantity)
        for quantity in cart.values()
    )


    return render(
        request,
        "cafe/home.html",
        {
            "products": products,
            "cart_count": cart_count,
            "search_query": search_query,
            "selected_category": category,
        }
    )


def add_to_cart(request, product_id):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request method."
            },
            status=400
        )

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if not product.is_available:
        return JsonResponse(
            {
                "success": False,
                "message": "This product is currently unavailable."
            },
            status=400
        )

    # IMPORTANT:
    # There is NO stock check here.
    # Stock is only the inventory/display value.
    # Customer can add the same product
    # multiple times to the cart.

    cart = request.session.get("cart", {})

    product_id_str = str(product_id)

    current_quantity = int(
        cart.get(
            product_id_str,
            0
        )
    )

    cart[product_id_str] = (
        current_quantity + 1
    )

    request.session["cart"] = cart
    request.session.modified = True

    cart_count = sum(
        int(quantity)
        for quantity in cart.values()
    )

    return JsonResponse(
        {
            "success": True,
            "message": f"{product.name} added to cart.",
            "cart_count": cart_count,
            "product_name": product.name,
            "stock": product.stock,
            "cart_quantity": cart[product_id_str],
        }
    )

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
def track_order(request):

    if request.method == "POST":

        order_id = request.POST.get("order_id", "").strip()

        if not order_id:
            return render(
                request,
                "cafe/track_order.html",
                {
                    "error": "Please enter your order number."
                }
            )

        try:

            order = Order.objects.get(
                id=int(order_id)
            )

            return redirect(
                "order_status",
                order_id=order.id
            )

        except (Order.DoesNotExist, ValueError):

            return render(
                request,
                "cafe/track_order.html",
                {
                    "error": "Order not found. Please check your order number."
                }
            )

    # Required for GET /track-order/
    return render(
        request,
        "cafe/track_order.html"
    )

def order_status(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related("items"),
        id=order_id
    )

    return render(
        request,
        "cafe/order_status.html",
        {
            "order": order
        }
    )