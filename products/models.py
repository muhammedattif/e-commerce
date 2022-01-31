from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import User
from django.db.models import JSONField, Q, Count
from categories.models import Category, Brand
from djmoney.models.fields import MoneyField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.utils import IntegrityError

def get_image_filename(instance, filename):
    id = instance.id
    return "product_images/%s-%s" % (id, filename)

# Product Model
class Product(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    description = RichTextUploadingField(blank=True)
    price = MoneyField(max_digits=14, decimal_places=4, default=1,
        validators=[
        MinValueValidator(1)
        ])

    discount = MoneyField(max_digits=14, decimal_places=4, default=0,
        validators=[
        MinValueValidator(0)
        ])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    creation = models.DateTimeField(blank=True, auto_now_add=True)
    # data = JSONField(db_index=True)

    class Meta:
        ordering = ('-creation',)

    def __str__(self):
        return self.name

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

    def get_relevant_products(self):
        return self.category.products.all()[:5]

class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    class Meta:
        unique_together = ('product', 'name')

    def __str__(self):
        return f'{self.product.name}-{self.name}'

class FeatureAttribute(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)
    additional_price = MoneyField(max_digits=14, decimal_places=4, default=0,
    validators=[
    MinValueValidator(0)
    ])

    def __str__(self):
        return f'{self.feature.product}-{self.feature.name}-{self.name}'

class FeatureAttributesMap(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features_attributes_maps')
    attributes = models.ManyToManyField(FeatureAttribute)
    quantity = models.PositiveSmallIntegerField(default=1,
        validators=[
        MinValueValidator(0)
        ])

    def __str__(self):
          return self.product.name


@receiver(m2m_changed, sender=FeatureAttributesMap.attributes.through)
def verify_uniqueness(sender, **kwargs):
    features_attribute_map = kwargs.get('instance', None)
    action = kwargs.get('action', None)
    attributes = kwargs.get('pk_set', None)
    attributes_len = len(attributes)

    if action == 'pre_add':
        quesrset = FeatureAttributesMap.objects.annotate(
                                                    total_attributes=Count('attributes'),
                                                    matching_attributes=Count('attributes', filter=Q(attributes__in=attributes))
                                                ).filter(
                                                    product=features_attribute_map.product,
                                                    matching_attributes=attributes_len,
                                                    total_attributes=attributes_len
                                                ).first()

        if quesrset:
            raise IntegrityError('Map with Product %s already exists for Attributes %s' % (features_attribute_map.product, attributes))


# Product Images Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to=get_image_filename)

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

    def __str__(self):
        return self.user.username
