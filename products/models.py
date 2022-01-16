from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import User
from django.db.models import JSONField

def get_image_filename(instance, filename):
    id = instance.id
    return "product_images/%s-%s" % (id, filename)

# Product Model
class Product(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    description = RichTextUploadingField(blank=True)
    price = models.IntegerField()
    discount = models.IntegerField()
    quantity = models.IntegerField(default=1)
    creation = models.DateTimeField(blank=True, auto_now_add=True)
    data = JSONField(db_index=True)
    def __str__(self):
        return self.name

class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('product', 'name')

    def __str__(self):
        return f'{self.product.name}-{self.name}'

class FeatureAttribute(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)



# Product Images Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_image_filename)

    def __str__(self):
        return self.product.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE, related_name="reviews")
    body = models.TextField(max_length=3000 , blank=True)
    rate = models.PositiveSmallIntegerField(default=0,
        validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
        ])

    likes= models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
