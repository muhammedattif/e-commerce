from django.db import models
from django.conf import settings
from products.models import Product

UserModel = settings.AUTH_USER_MODEL


class CartItem(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}-{self.product}'
