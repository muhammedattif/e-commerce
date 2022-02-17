from django.db import models
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import User
from django.db.models import JSONField, Q, Count, Sum, F
from categories.models import Category, Brand
from djmoney.models.fields import MoneyField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import src.utils as general_utils

User = get_user_model()

def get_image_filename(instance, filename):
    id = instance.id
    return "product_images/%s-%s" % (id, filename)

# Product Model
class Product(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.RESTRICT)
    name = models.TextField()
    description = RichTextUploadingField(blank=True)
    cover = models.ImageField(upload_to=get_image_filename)
    price = MoneyField(max_digits=14, decimal_places=4, default=1,
        validators=[
        MinMoneyValidator(1)
        ], default_currency='SAR')

    discount = MoneyField(max_digits=14, decimal_places=4, default=0,
        validators=[
        MinMoneyValidator(0)
        ], default_currency='SAR')
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_DEFAULT, default=1, related_name="products")
    creation = models.DateTimeField(blank=True, auto_now_add=True)
    minimum_cart_quantity = models.PositiveIntegerField(default=1)
    code = models.CharField(blank=True, max_length=100, default=general_utils.generate_random_string)

    class Meta:
        ordering = ('-creation',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_random_string()
        super(Product, self).save(*args, **kwargs)

    def get_rating(self):
        total_reviews = self.reviews.count()
        if not total_reviews:
            return 0

        reviews = self.reviews.all()

        _5_star_reviews = 0
        _4_star_reviews = 0
        _3_star_reviews = 0
        _2_star_reviews = 0
        _1_star_reviews = 0
        for review in reviews:
            if review.rate == 5:
                _5_star_reviews += 1
            elif review.rate == 4:
                _4_star_reviews += 1
            elif review.rate == 3:
                _3_star_reviews += 1
            elif review.rate == 2:
                _2_star_reviews += 1
            elif review.rate == 1:
                _1_star_reviews += 1

        total_score = _5_star_reviews*5 + _4_star_reviews*4 + _3_star_reviews*3 + _2_star_reviews*2 + _1_star_reviews*1

        return round(total_score/total_reviews, 1)

    def get_quantity(self):
        quantity = self.stock.aggregate(sum=Sum(F('quantity')))['sum']
        return quantity

    def get_relevant_products(self):
        return self.category.products.all()[:5]

class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('product', 'name')
        verbose_name = _('Feature')
        verbose_name_plural = _('Features')

    def __str__(self):
        return f'{self.product.name}-{self.name}'

class FeatureOption(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    additional_price = MoneyField(max_digits=14, decimal_places=4, default=0,
    validators=[
    MinMoneyValidator(0)
    ], default_currency='SAR')

    class Meta:
        unique_together = ('feature', 'name')
        verbose_name = _('Feature Option')
        verbose_name_plural = _('Feature Options')

    def __str__(self):
        return f'{self.feature.product}-{self.feature.name}-{self.name}'


# Product Images Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to=get_image_filename)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')

    def __str__(self):
        return self.product.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE, related_name="reviews")
    body = models.TextField(max_length=3000)
    rate = models.PositiveSmallIntegerField(default=1,
        validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
        ])

    likes= models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='favorite')
    products = models.ManyToManyField(Product)

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')

    def __str__(self):
        return self.user.username
