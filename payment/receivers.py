from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from payment.models import Cart, CartItem
from django.db.models import Sum
from decimal import Decimal
from djmoney.money import Money

UserModel = settings.AUTH_USER_MODEL

# Not used
# @receiver(post_save, sender=Cart)
# def calculate_item_price(sender, instance=None, created=False, **kwargs):
#     if created:
#         # calculate original price including Taxes
#         original_price = instance.product.price
#         discount = instance.product.discount
#         additional_price = instance.stock.options.aggregate(sum=Sum('additional_price'))['sum']
#         final_price = ((original_price.amount-discount.amount) + additional_price * (1 + Decimal(settings.TAX_AMOUNT)/Decimal(100.0))) * instance.quantity
#         instance.final_price = final_price
#
#         # Update Cart Prices Values
#         instance.cart.sub_total.amount += (final_price + (discount.amount * instance.quantity))
#         instance.cart.total.amount += final_price
#         instance.cart.discount += discount*instance.quantity
#         instance.cart.save()
#         instance.save()
