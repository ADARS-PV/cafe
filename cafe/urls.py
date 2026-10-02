from django.urls import path
from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Add product to cart
    path(
        "add-to-cart/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    # Cart
    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    # Increase cart quantity
    path(
        "cart/increase/<int:product_id>/",
        views.increase_cart,
        name="increase_cart"
    ),

    # Decrease cart quantity
    path(
        "cart/decrease/<int:product_id>/",
        views.decrease_cart,
        name="decrease_cart"
    ),

    # Remove from cart
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # Customer order status
    path(
        "order/<int:order_id>/status/",
        views.order_status,
        name="order_status"
    ),

    # Customer track order
    path(
        "track-order/",
        views.track_order,
        name="track_order"
    ),

]