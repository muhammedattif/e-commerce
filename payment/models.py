from django.db import models
from djmoney.models.validators import MinMoneyValidator
from django.core.validators import MinValueValidator
from djmoney.models.fields import MoneyField
from django.conf import settings
from products.models import Product
from vendor.models import Stock
from users.models import Address
from django.db.models.functions import Coalesce
from django.db.models import Sum, F, FloatField
from decimal import Decimal
from django.utils.translation import gettext_lazy as _

UserModel = settings.AUTH_USER_MODEL


class Cart(models.Model):
    user = models.OneToOneField(UserModel, verbose_name = _('User'), on_delete=models.CASCADE, related_name='cart')
    total = MoneyField(max_digits=14, decimal_places=4, default=0, null=True, blank=True, default_currency='SAR', verbose_name = _('Total'))
    sub_total = MoneyField(max_digits=14, decimal_places=4, default=0, null=True, blank=True, default_currency='SAR', verbose_name = _('Sub total'))
    discount = MoneyField(max_digits=14, decimal_places=4, default=0, null=True, blank=True, default_currency='SAR', verbose_name = _('Discount'))
    taxes = MoneyField(max_digits=14, decimal_places=4, default=0, default_currency='SAR', verbose_name = _('Taxes'))
    creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f'{self.user.username}'

    def calculate_sub_total(self):
        sub_total = self.items.aggregate( sum=Coalesce(Sum(F('product__price') * F('quantity')), 0, output_field=FloatField()) )['sum']
        additional_price = self.items.aggregate(sum=Coalesce(Sum(F('stock__options__additional_price') * F('quantity')), 0, output_field=FloatField()))['sum']
        self.sub_total = sub_total + additional_price
        return self.sub_total

    def calculate_discount(self):
        self.discount = self.items.aggregate(sum=Coalesce(Sum( F('product__discount') * F('quantity') ), 0, output_field=FloatField()) )['sum']
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
    product = models.ForeignKey(Product, verbose_name = _('Product'), on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name = _('Cart'), on_delete=models.CASCADE, related_name='items')
    stock = models.ForeignKey(Stock, verbose_name = _('Stock'), on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=False, default=1, validators=[
    MinValueValidator(1)
    ], verbose_name = _('Quantity'))

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def __str__(self):
        return f'{self.product.name}-{self.stock.id}'
