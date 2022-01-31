from django.db import models
from django.core.validators import MinValueValidator
from djmoney.models.fields import MoneyField
from django.conf import settings
from products.models import Product, FeatureAttributesMap
from users.models import Address

UserModel = settings.AUTH_USER_MODEL


class Cart(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='cart')
    total = MoneyField(max_digits=14, decimal_places=4, default=0, null=True, blank=True)
    sub_total = MoneyField(max_digits=14, decimal_places=4, default=0, null=True, blank=True)
    discount = MoneyField(max_digits=14, decimal_places=4, default=0, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'

    def clear(self):
        self.total = 0
        self.sub_total = 0
        self.discount = 0
        self.items.all().delete()
        return True

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    attributes_map = models.ForeignKey(FeatureAttributesMap, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=False, default=1, validators=[
    MinValueValidator(1)
    ])

    TAX_AMOUNT = 14.0

    def __str__(self):
        return self.product.name

    def get_final_price(self):
        return self.product.price * (1 + self.TAX_AMOUNT/100.0)



class Order(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='orders')
    address =models.ForeignKey(Address, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total = MoneyField(max_digits=14, decimal_places=4)
    sub_total = MoneyField(max_digits=14, decimal_places=4)
    discount = MoneyField(max_digits=14, decimal_places=4, default=0)

    def __str__(self):
          return self.user.username
