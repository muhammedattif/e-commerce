from django.db import models
from django.db.models import Q, Count
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from products.models import Product, FeatureOption
from django.core.validators import MinValueValidator
from django.db.utils import IntegrityError
import src.utils as general_utils

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    options = models.ManyToManyField(FeatureOption)
    quantity = models.PositiveSmallIntegerField(default=1,
        validators=[
        MinValueValidator(0)
        ])

    class Meta:
        ordering = ['-id']

    def __str__(self):
          return self.product.name


@receiver(m2m_changed, sender=Stock.options.through)
def verify_uniqueness(sender, **kwargs):
    stock = kwargs.get('instance', None)
    action = kwargs.get('action', None)
    options = kwargs.get('pk_set', None)
    options_len = len(options)

    if action == 'pre_add':
        queryset = Stock.objects.annotate(
                                                    total_options=Count('options'),
                                                    matching_options=Count('options', filter=Q(options__in=options))
                                                ).filter(
                                                    product=stock.product,
                                                    matching_options=options_len,
                                                    total_options=options_len
                                                )
        if queryset:
            raise IntegrityError('Stock with Product %s already exists for options %s' % (stock.product, options))

@receiver(pre_save, sender=Stock)
def verify_uniqueness(sender, instance=None, **kwargs):

    stock = Stock.objects.filter(product=instance.product, options=None)
    if stock:
        raise IntegrityError(general_utils.error_messages['stock_already_exists'])
