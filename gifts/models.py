from django.db import models
from django.db.models import F
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from djmoney.models.fields import MoneyField
import datetime
from datetime import date
import random
from categories.models import Category, Brand
User = get_user_model()

class PromoCode(models.Model):
    name = models.CharField(max_length=8)

    discount_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='promo_code')
    discount_object_id = models.PositiveIntegerField()
    discount_object = GenericForeignKey('discount_type', 'discount_object_id')

    valid_from = models.DateField(default=datetime.datetime.today)
    valid_untill = models.DateField(default=datetime.datetime.today)

    maximum_usage = models.PositiveIntegerField(default=1, help_text = "If set to 0, it means unlimited.")
    number_of_uses = models.PositiveIntegerField(default=0)
    usage_limit_for_user = models.PositiveIntegerField(default=1, help_text = "If set to 0, it means unlimited.")

    active = models.BooleanField(default=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text = "If set to Null, it means general.")

    def __str__(self):
        return self.name

    def is_active(self):
        return self.active

    def is_expired(self):
        return self.valid_untill < date.today()

    def is_valid(self):
        return self.is_active() and not self.is_expired()

    def is_limit_reached(self):
        return self.number_of_uses >= self.maximum_usage or not self.maximum_usage

    def is_owner(self, user):
        return user == self.owner or not self.owner

    def is_owner_limit_reached(self, owner):
        return self.redemptions.filter(user=owner).count() >= self.usage_limit_for_user or not self.usage_limit_for_user

    def redeem(self, user):

        if self.is_limit_reached() or self.is_owner_limit_reached(user):
            return False

        redemption = Redemption.objects.create(user=user, promo_code=self)
        if not redemption:
            return False

        self.number_of_uses = F('number_of_uses') + 1
        self.save(update_fields=['number_of_uses'])
        return True

    def check_conditions(self, order_amount):
        conditions_result = True
        for condition in self.rules.conditions.all():
            condition_rule = Condition(order_amount, str(condition.operator),
                                       condition.price.amount)
            conditions_result = True if conditions_result and condition_rule.run() else False
        return conditions_result

    def check_brands(self, brands):
        pass

    def check_categories(self, categories):
        pass

import operator
class Condition:
    """
    This a class that is made for dynamic if conditions
    """
    OPERATOR_SYMBOLS = {
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge
    }

    def __init__(self, value1, op, value2):
        self.value1 = value1
        self.op = op
        self.value2 = value2

    def run(self):
        return self.OPERATOR_SYMBOLS[self.op](self.value1, self.value2)


class PromoCodeCondition(models.Model):
    operator = models.CharField(max_length=1)
    price = MoneyField(max_digits=14, decimal_places=4, default=10,
        validators=[
        MinMoneyValidator(1)
        ], default_currency='SAR')

class PromoCodeRule(models.Model):
    promo_code = models.OneToOneField(PromoCode, on_delete=models.CASCADE, related_name='rules')
    allowed_categories = models.ManyToManyField(Category, help_text = "If set to Null, it means general.")
    allowed_brands = models.ManyToManyField(Brand, help_text = "If set to Null, it means general.")
    conditions = models.ManyToManyField(PromoCodeCondition, help_text = "If set to Null, it means general.")

class Redemption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='redemptions')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name='redemptions')
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class FixedDiscount(models.Model):
    amount = MoneyField(max_digits=14, decimal_places=4, default=10,
        validators=[
        MinMoneyValidator(1)
        ], default_currency='SAR')

    def __str__(self):
        return str(self.id)


class PercentageDiscount(models.Model):
    percentage = models.PositiveIntegerField()
    max_discount_limit = MoneyField(max_digits=14, decimal_places=4, default=100,
        validators=[
        MinMoneyValidator(1)
        ], default_currency='SAR')

    def __str__(self):
        return str(self.id)
