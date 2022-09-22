from django.db import models
from account.models import User
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    qty_in_stock = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    payment_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.email} ordered {self.product.name} on {self.date_created}"
