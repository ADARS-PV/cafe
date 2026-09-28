from django.urls import path

from . import views


app_name = "staff"


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "login/",
        views.staff_login,
        name="login"
    ),

    path(
        "logout/",
        views.staff_logout,
        name="logout"
    ),

    path(
        "orders/",
        views.orders,
        name="orders"
    ),

    path(
        "orders/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

    path(
        "orders/<int:order_id>/status/",
        views.update_order_status,
        name="update_order_status"
    ),

    path(
        "products/",
        views.products,
        name="products"
    ),

    path(
        "products/add/",
        views.add_product,
        name="add_product"
    ),

    path(
        "products/<int:product_id>/edit/",
        views.edit_product,
        name="edit_product"
    ),

    path(
        "products/<int:product_id>/delete/",
        views.delete_product,
        name="delete_product"
    ),

    path(
        "daily-report/",
        views.daily_report,
        name="daily_report"
    ),
]