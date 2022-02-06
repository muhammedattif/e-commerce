from django.db import models
from django.core.validators import MinValueValidator
from djmoney.models.fields import MoneyField
from django.conf import settings
from django.db.models import Sum, F
from products.models import Product
from vendor.models import Stock
from users.models import Address
UserModel = settings.AUTH_USER_MODEL

class Order(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='orders')
    address =models.ForeignKey(Address, on_delete=models.CASCADE)
    total = MoneyField(max_digits=14, decimal_places=4, default_currency='SAR')
    sub_total = MoneyField(max_digits=14, decimal_places=4, default_currency='SAR')
    discount = MoneyField(max_digits=14, decimal_places=4, default=0, default_currency='SAR')
    taxes = MoneyField(max_digits=14, decimal_places=4, default=0, default_currency='SAR')
    creation = models.DateTimeField(auto_now_add=True)

    # Order Tracking Status
    is_processed = models.BooleanField(default=True)
    is_shipped = models.BooleanField(default=False)
    is_in_route = models.BooleanField(default=False)
    is_arrived = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
          return self.user.username


    def cancel(self):
        self.is_cancelled = True

        order_items = self.items.all()
        for item in order_items:
            item.stock.quantity = F('quantity') + item.quantity
            item.stock.save()
        self.save()

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=False, default=1, validators=[
    MinValueValidator(1)
    ])

    def __str__(self):
        return f'{self.product.name}-{self.stock.id}'
