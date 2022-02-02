from django.db import models
from django.db.models import Q, Count
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from products.models import Product, FeatureAttribute
from django.core.validators import MinValueValidator
from django.db.utils import IntegrityError
import src.utils as general_utils

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    attributes = models.ManyToManyField(FeatureAttribute)
    quantity = models.PositiveSmallIntegerField(default=1,
        validators=[
        MinValueValidator(0)
        ])

    class Meta:
        ordering = ['-id']

    def __str__(self):
          return self.product.name


@receiver(m2m_changed, sender=Stock.attributes.through)
def verify_uniqueness(sender, **kwargs):
    stock = kwargs.get('instance', None)
    action = kwargs.get('action', None)
    attributes = kwargs.get('pk_set', None)
    attributes_len = len(attributes)

    if action == 'pre_add':
        queryset = Stock.objects.annotate(
                                                    total_attributes=Count('attributes'),
                                                    matching_attributes=Count('attributes', filter=Q(attributes__in=attributes))
                                                ).filter(
                                                    product=stock.product,
                                                    matching_attributes=attributes_len,
                                                    total_attributes=attributes_len
                                                )
        if queryset:
            raise IntegrityError('Stock with Product %s already exists for Attributes %s' % (stock.product, attributes))

@receiver(pre_save, sender=Stock)
def verify_uniqueness(sender, instance=None, **kwargs):

    stock = Stock.objects.filter(product=instance.product, attributes=None)
    if stock:
        raise IntegrityError(general_utils.error_messages['stock_already_exists'])
