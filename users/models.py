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

    def create_user(self, email, username, first_name, last_name, avatar='', location='', password=None, is_staff=False, is_superuser=False, is_vendor=False):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise VlaueError('User must have a username')

        user = self.model(
                        email=self.normalize_email(email),
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        avatar=avatar,
                        location=location,
                        is_staff=is_staff,
                        is_superuser=is_superuser,
                        is_vendor=is_vendor
                        )


        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, email, username, password, first_name, last_name, avatar=None, location=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
            location=location,
            is_staff = True,
            is_vendor = True,
            is_superuser = True
        )
        user.save(using = self._db)
        return user

# Account Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True, verbose_name = _('Email'))
    first_name = models.CharField(max_length=30, verbose_name = _('First Name'))
    last_name = models.CharField(max_length=30, verbose_name = _('Last Name'))
    username = models.CharField(max_length=30, unique=True, validators=[UnicodeUsernameValidator()], verbose_name = _('Username'))
    avatar = models.ImageField(upload_to=get_image_filename, verbose_name = _('Avatar'), blank=True)
    location = models.CharField(max_length=100, verbose_name = _('Location'), blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name = _('Date Joined'))
    last_login = models.DateTimeField(auto_now=True, verbose_name = _('Last Login'))
    is_active = models.BooleanField(default=True, verbose_name = _('Active Status'))
    is_staff = models.BooleanField(default=False, verbose_name = _('Staff Status'))
    is_vendor = models.BooleanField(default=False, verbose_name = _('Vendor status'))

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta(AbstractBaseUser.Meta, PermissionsMixin.Meta):
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    # resize profile image before saving
    def save(self, created=None, *args, **kwargs):
        super().save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(User, verbose_name = _('User'), on_delete=models.CASCADE, related_name="addresses")
    locality = models.CharField(max_length = 200, verbose_name = _('Locality'))
    city = models.CharField(max_length=50, verbose_name = _('City'))
    zipcode = models.IntegerField(verbose_name = _('Zipcode'))
    state = models.CharField(max_length=50, verbose_name = _('State'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f'{self.user.username}->{self.city}'
