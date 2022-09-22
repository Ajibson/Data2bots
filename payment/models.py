from django.db import models
from account.models import User
from product.models import Order
from django.utils import timezone


class Payment(models.Model):
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_for = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.order.user.email} initiated the payment of {self.amount}"
