from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.db.models import F
from django.db import transaction

def get_image_filename(instance, filename):
    id = instance.id
    return "profile_images/%s/%s" % (id, filename)

# this class is for overriding default users manager of django user model
class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, is_staff=False, is_superuser=False, is_vendor=False):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise VlaueError('User must have a username')

        is_active = True
        # if is_vendor:
        #     is_active = False

        user = self.model(
                        email=self.normalize_email(email),
                        username=username,
                        is_active=is_active,
                        is_staff=is_staff,
                        is_superuser=is_superuser,
                        is_vendor=is_vendor
        )


        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            is_staff = True,
            is_vendor = True,
            is_superuser = True
        )
        user.save(using = self._db)
        return user

# Account Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True, validators=[UnicodeUsernameValidator()])
    avatar = models.ImageField(upload_to=get_image_filename, null=True, blank=True)
    location = models.CharField(blank=True, max_length=100)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_active = models.BooleanField('Active status', default=True)
    is_staff = models.BooleanField('Staff status', default=False)
    is_vendor = models.BooleanField('Vendor status', default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # resize profile image before saving
    def save(self, created=None, *args, **kwargs):
        super().save(*args, **kwargs)


class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    locality = models.CharField(max_length = 200)
    city = models.CharField(max_length = 50)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "addresses"



class Student(models.Model):

    YEAR_IN_SCHOOL_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]
    ACADEMIC_YEAR = [
        (1, 'FIRST'),
        (2, 'SECOND'),
        (3, 'THIRD'),
        (4, 'FOURTH'),
        (5, 'FIFTH'),
        (6, 'SIXTH'),
        (7, 'SEVENTH'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name="student_info")
    major = models.CharField(blank=True, null=True, max_length=40)
    academic_year = models.IntegerField(blank=True, null=True, choices=ACADEMIC_YEAR)
    year_in_school = models.CharField(max_length=20, blank=True, null=True, choices=YEAR_IN_SCHOOL_CHOICES)

    def __str__(self):
        return self.user.email

    def is_enrolled(self, course):
        return course.id in self.user.courses_enrollments.values_list('course', flat=True)

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name="teacher_info")
    major = models.CharField(blank=True, max_length=40)

    def __str__(self):
        return self.user.email
