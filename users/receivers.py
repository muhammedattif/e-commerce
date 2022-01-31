from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VendorProfile, CustomerProfile
from rest_framework.authtoken.models import Token
from django.conf import settings
from payment.models import Cart

UserModel = settings.AUTH_USER_MODEL

@receiver(post_save, sender=UserModel)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.is_vendor:
            VendorProfile.objects.create(user=instance)
        else:
            CustomerProfile.objects.create(user=instance)

@receiver(post_save, sender=UserModel)
def create_user_cart(sender, instance=None, created=False, **kwargs):
    if created:
        Cart.objects.create(user=instance)
