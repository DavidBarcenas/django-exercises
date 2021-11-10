from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Payment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_id = models.CharField(max_length=200)
    payer_id = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.price
