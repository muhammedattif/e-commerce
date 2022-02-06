from django.db import models
from djmoney.models.validators import MinMoneyValidator
from django.core.validators import MinValueValidator
from djmoney.models.fields import MoneyField
from django.conf import settings
from products.models import Product
from vendor.models import Stock
from users.models import Address
from django.db.models import Sum, F
from decimal import Decimal

UserModel = settings.AUTH_USER_MODEL


class Cart(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='cart')
    total = MoneyField(max_digits=14, decimal_places=4, default=0, null=True, blank=True, default_currency='SAR')
    sub_total = MoneyField(max_digits=14, decimal_places=4, default=0, null=True, blank=True, default_currency='SAR')
    discount = MoneyField(max_digits=14, decimal_places=4, default=0, null=True, blank=True, default_currency='SAR')
    taxes = MoneyField(max_digits=14, decimal_places=4, default=0, default_currency='SAR')
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'

    def calculate_sub_total(self):
        sub_total = self.items.aggregate(sum=Sum(F('product__price') * F('quantity')))['sum']
        additional_price = self.items.aggregate(sum=Sum(F('stock__options__additional_price') * F('quantity')))['sum']
        print(additional_price)
        self.sub_total = sub_total + additional_price
        return self.sub_total

    def calculate_discount(self):
        self.discount = self.items.aggregate(sum=Sum( F('product__discount') * F('quantity') ))['sum']
        return self.discount

    def calculate_total(self):
        self.total = self.sub_total - self.discount
        return self.total

    def calculate_taxes(self):
        self.taxes = (self.total * (Decimal(settings.TAX_AMOUNT)/Decimal(100.0)))
        return self.taxes

    def recalculate_cart_amount(self):
        self.calculate_sub_total()
        self.calculate_total()
        self.calculate_discount()
        self.calculate_taxes()
        self.save()

    def clear(self):
        self.total = 0
        self.sub_total = 0
        self.discount = 0
        self.taxes = 0
        self.items.all().delete()
        self.save()
        return True



class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=False, default=1, validators=[
    MinValueValidator(1)
    ])

    def __str__(self):
        return f'{self.product.name}-{self.stock.id}'
