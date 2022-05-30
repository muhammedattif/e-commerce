from django.db import models
from django.db.models import Q, Count
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver
from products.models import Product, FeatureOption
from django.core.validators import MinValueValidator
from django.db.utils import IntegrityError
import src.utils as general_utils
from django.utils.translation import gettext_lazy as _


class JoinForm(models.Model):
    agent_name = models.CharField(_('Agent Name'), max_length=100)
    vendor_name = models.CharField(_('Vendor Name'), max_length=100)
    email = models.CharField(_('Email'), max_length=100)
    phone_number = models.CharField(_('Phone Number'), unique=True, max_length=100)

    def __str__(self):
        return self.vendor_name

class Stock(models.Model):
    product = models.ForeignKey(Product, verbose_name = _('Product'), on_delete=models.RESTRICT, related_name='stock')
    options = models.ManyToManyField(FeatureOption, blank=True, verbose_name = _('Option'))
    quantity = models.PositiveSmallIntegerField(default=1,
        validators=[
        MinValueValidator(0)
        ], verbose_name = _('Quantity'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')


    def __str__(self):
          return self.product.name


def verify_uniqueness(stock, options):

    options_len = len(options)
    if options:
        stock_obj = Stock.objects.annotate(
                                                    total_options=Count('options'),
                                                    matching_options=Count('options', filter=Q(options__in=options))
                                                ).filter(
                                                    product=stock.product,
                                                    matching_options=options_len,
                                                    total_options=options_len
                                                )
    else:
        stock_obj = Stock.objects.filter(product=stock.product, options=None)
    if stock_obj:
        return True
    return False



@receiver(m2m_changed, sender=Stock.options.through)
def verify_uniqueness_on_update(sender, **kwargs):

    action = kwargs.get('action', None)
    if action == 'pre_add':
        stock = kwargs.get('instance', None)
        options = kwargs.get('pk_set', None)
        exists = verify_uniqueness(stock, options)
        if exists:
            raise IntegrityError(general_utils.error_messages['stock_already_exists'])
