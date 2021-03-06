from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.db.models import F
from django.db import transaction
from django.utils.translation import gettext_lazy as _

def get_image_filename(instance, filename):
    id = instance.id
    return "profile_images/%s/%s" % (id, filename)

# this class is for overriding default users manager of django user model
class MyAccountManager(BaseUserManager):

    def create_user(self, email, phone_number, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        if not phone_number:
            raise VlaueError('User must have a phone number')

        user = self.model(
                        email=self.normalize_email(email),
                        phone_number=phone_number,
                        **extra_fields
                        )


        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, email, phone_number, password, first_name, last_name, avatar=None, location=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
            location=location,
            is_staff = True,
            reg_as_vendor = False,
            is_superuser = True
        )
        user.save(using = self._db)
        return user

# Account Model
class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(unique=True, max_length=100, null=True)
    email = models.EmailField(max_length=60, unique=True, verbose_name=_('Email'))
    first_name = models.CharField(max_length=30, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=30, verbose_name=_('Last Name'))
    agent_name = models.CharField(max_length=30, verbose_name=_('Agent Name'), blank=True)
    location = models.CharField(max_length=100, verbose_name=_('Location'), blank=True)
    city = models.CharField(max_length=100, verbose_name=_('City'), blank=True)
    district = models.CharField(max_length=100, verbose_name=_('District Name'), blank=True)
    avatar = models.ImageField(upload_to=get_image_filename, verbose_name=_('Avatar'), blank=True)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Joined'))
    last_login = models.DateTimeField(auto_now=True, verbose_name=_('Last Login'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active Status'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff Status'))
    reg_as_vendor = models.BooleanField(default=False, verbose_name=_('Registered as vendor'))

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    class Meta(AbstractBaseUser.Meta, PermissionsMixin.Meta):
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    # resize profile image before saving
    def save(self, created=None, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def is_active_vendor(self):
        return Vendor.objects.filter(user=self, is_active=True).exists()

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_status')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class Address(models.Model):
    user = models.ForeignKey(User, verbose_name = _('User'), on_delete=models.CASCADE, related_name="addresses")
    locality = models.CharField(max_length = 200, verbose_name = _('Locality'))
    city = models.CharField(max_length=50, verbose_name = _('City'))
    zipcode = models.IntegerField(verbose_name = _('Zipcode'))
    state = models.CharField(max_length=50, verbose_name = _('State'))
    phone_number = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f'{self.user.email}->{self.city}'
