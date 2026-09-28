from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = [
        ("HOT", "Hot"),
        ("COOL", "Cool"),
        ("SNACKS", "Snacks"),
    ]

    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="SNACKS"
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class Order(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Preparing", "Preparing"),
        ("Ready", "Ready"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    table_name = models.CharField(
        max_length=100
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - Table {self.table_name}"

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):

        if self.price is None:
            return 0

        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"