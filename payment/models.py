from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings
from products.models import Product, FeatureAttribute
from users.models import Address

UserModel = settings.AUTH_USER_MODEL



class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attributes = models.ManyToManyField(FeatureAttribute)
    creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=False, default=1)

    TAX = 0.14

    def __str__(self):
        return self.product.name

    def get_final_price(self):
        return self.product.price*self.quantity*self.TAX


class Cart(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(CartItem)
    total = MoneyField(max_digits=14, decimal_places=4)
    sub_total = MoneyField(max_digits=14, decimal_places=4)
    discount = MoneyField(max_digits=14, decimal_places=4, default=0)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'



class Order(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='orders')
    address =models.ForeignKey(Address, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total = MoneyField(max_digits=14, decimal_places=4)
    sub_total = MoneyField(max_digits=14, decimal_places=4)
    discount = MoneyField(max_digits=14, decimal_places=4, default=0)

    def __str__(self):
          return self.user.username
