from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from cafe.models import Product, Order, OrderItem

from .forms import ProductForm, StaffLoginForm


# ============================================================
# STAFF PERMISSION
# ============================================================

def is_staff(user):
    return user.is_authenticated and user.is_staff


staff_required = user_passes_test(
    is_staff,
    login_url="/staff/login/"
)


# ============================================================
# STAFF LOGIN
# ============================================================

def staff_login(request):

    # Already logged in
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("staff:dashboard")

    if request.method == "POST":

        form = StaffLoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("staff:dashboard")

    else:

        form = StaffLoginForm()

    return render(
        request,
        "staff/login.html",
        {
            "form": form
        }
    )


# ============================================================
# STAFF LOGOUT
# ============================================================

@staff_required
def staff_logout(request):

    logout(request)

    return redirect("staff:login")


# ============================================================
# DASHBOARD
# ============================================================

@staff_required
def dashboard(request):

    today = timezone.localdate()

    today_orders = Order.objects.filter(
        created_at__date=today
    )

    collection = (
        today_orders
        .exclude(status="Cancelled")
        .aggregate(
            total=Sum("total_amount")
        )["total"]
        or Decimal("0")
    )

    recent_orders = today_orders.order_by(
        "-created_at"
    )[:10]

    context = {
        "today": today,

        "total_orders": today_orders.count(),

        "pending_orders": today_orders.filter(
            status="Pending"
        ).count(),

        "preparing_orders": today_orders.filter(
            status="Preparing"
        ).count(),

        "ready_orders": today_orders.filter(
            status="Ready"
        ).count(),

        "completed_orders": today_orders.filter(
            status="Completed"
        ).count(),

        "cancelled_orders": today_orders.filter(
            status="Cancelled"
        ).count(),

        "collection": collection,

        "recent_orders": recent_orders,
    }

    return render(
        request,
        "staff/dashboard.html",
        context
    )


# ============================================================
# ORDERS
# ============================================================

@login_required(login_url="staff:login")
def orders(request):

    today = timezone.localdate()

    orders = (
        Order.objects
        .filter(created_at__date=today)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    today_collection = (
        orders.aggregate(
            total=Sum("total_amount")
        )["total"] or 0
    )

    pending_orders = orders.filter(
        status__in=["Pending", "PENDING"]
    ).count()

    return render(
        request,
        "staff/orders.html",
        {
            "orders": orders,
            "today": today,
            "today_collection": today_collection,
            "pending_orders": pending_orders,
        }
    )

# ============================================================
# ORDER DETAIL
# ============================================================

@login_required(login_url="staff:login")
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product"
        ),
        id=order_id
    )

    if request.method == "POST":

        status = request.POST.get("status")

        if status:
            order.status = status
            order.save(update_fields=["status"])

        return redirect(
            "staff:order_detail",
            order_id=order.id
        )

    return render(
        request,
        "staff/order_detail.html",
        {
            "order": order,
        }
    )


# ============================================================
# UPDATE ORDER STATUS
# ============================================================

@staff_required
def update_order_status(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        status = request.POST.get("status")

        valid_statuses = [
            "Pending",
            "Preparing",
            "Ready",
            "Completed",
            "Cancelled",
        ]

        if status in valid_statuses:

            order.status = status
            order.save()

            messages.success(
                request,
                f"Order #{order.id} updated successfully."
            )

    return redirect(
        "staff:order_detail",
        order_id=order.id
    )


# ============================================================
# PRODUCTS
# ============================================================

@staff_required
def products(request):

    products = Product.objects.all().order_by(
        "-created_at"
    )

    search = request.GET.get("search")
    category = request.GET.get("category")

    if search:

        products = products.filter(
            name__icontains=search
        )

    if category:

        products = products.filter(
            category=category
        )

    return render(
        request,
        "staff/products.html",
        {
            "products": products,
            "search": search or "",
            "category": category or "",
        }
    )


# ============================================================
# ADD PRODUCT
# ============================================================

@staff_required
def add_product(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect(
                "staff:products"
            )

    else:

        form = ProductForm()

    return render(
        request,
        "staff/product_form.html",
        {
            "form": form,
            "title": "Add Product",
        }
    )


# ============================================================
# EDIT PRODUCT
# ============================================================

@staff_required
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "staff:products"
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "staff/product_form.html",
        {
            "form": form,
            "product": product,
            "title": "Edit Product",
        }
    )


# ============================================================
# DELETE PRODUCT
# ============================================================

@staff_required
def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

    return redirect(
        "staff:products"
    )


# ============================================================
# DAILY REPORT
# ============================================================

@login_required
def daily_report(request):

    today = timezone.localdate()

    orders = (
        Order.objects
        .filter(created_at__date=today)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    total_orders = orders.count()

    total_collection = (
        orders.aggregate(
            total=Sum("total_amount")
        )["total"] or 0
    )

    total_items = 0

    for order in orders:
        for item in order.items.all():
            total_items += item.quantity

    if total_orders:
        average_order = total_collection / total_orders
    else:
        average_order = 0

    context = {
        "orders": orders,
        "report_date": today,
        "total_orders": total_orders,
        "total_collection": total_collection,
        "total_items": total_items,
        "average_order": average_order,
    }

    return render(
        request,
        "staff/daily_report.html",
        context
    )