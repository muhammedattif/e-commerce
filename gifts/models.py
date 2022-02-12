from django.db import models, transaction
from django.db.models import F
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from djmoney.models.fields import MoneyField
from django.db import IntegrityError
import datetime
from datetime import date
import random
from categories.models import Category, Brand
import random
from .utils import Condition, PromoCodeConfig
from django.utils import timezone
from .settings import (
    COUPON_TYPES,
    CODE_LENGTH,
    CODE_CHARS,
    SEGMENTED_CODES,
    SEGMENT_LENGTH,
    SEGMENT_SEPARATOR,
)

User = get_user_model()
from dataclasses import astuple, dataclass

class PromoCodeManager(models.Manager):

    @transaction.atomic
    def create_promo_code(
    self,
    config: PromoCodeConfig
    ):
        discount_type = config.discount_type
        amount = config.amount
        percentage = config.percentage
        max_discount_limit = config.max_discount_limit
        users = config.users
        all_users = config.all_users
        code = config.code
        valid_from = config.valid_from
        valid_until = config .valid_until
        is_active = config.is_active
        prefix = config.prefix
        max_uses = config.max_uses
        is_infinite = config.is_infinite
        usage_limit_per_user = config.usage_limit_per_user
        user_usage_is_infinite = config.user_usage_is_infinite
        categories = config.categories
        brands = config.brands
        conditions = config.conditions

        if discount_type =='fixed':
            discount_type = ContentType.objects.get(model='fixeddiscount')
            discount_object = FixedDiscount(amount=amount)
        else:
            discount_type = ContentType.objects.get(model='percentagediscount')
            discount_object = PercentageDiscount(percentage=percentage, max_discount_limit=max_discount_limit)
        discount_object.save()


        if not code:
            code = PromoCode.generate_code()

        try:
            promo_code = self.create(
                code=code,
                discount_type=discount_type,
                discount_object=discount_object,
                discount_object_id=discount_object.id,
            )

        except IntegrityError:
            raise (f'Promo Code with -> {code} is already exists')

        # Create Allowed Users Rule
        if not isinstance(users, list):
            users = [users]

        allowed_users = AllowedUsersRule(all_users=all_users)
        allowed_users.save()
        allowed_users.users.add(*users)

        # Create Usage Rule
        usage_rule = UsageRule(
                max_uses=max_uses,
                is_infinite=is_infinite,
                usage_limit_per_user=usage_limit_per_user,
                user_usage_is_infinite=user_usage_is_infinite
        )
        usage_rule.save()

        # Create Validity Rule
        validity_rule = ValidityRule(valid_from=valid_from, valid_until=valid_until, is_active=is_active)
        validity_rule.save()

        promo_code_rule = PromoCodeRule(
        promo_code=promo_code,
        allowed_users=allowed_users,
        validity=validity_rule,
        usage=usage_rule
        )
        promo_code_rule.save()

        # Set Categories Rule
        promo_code_rule.allowed_categories.add(*categories)

        # Set Brands Rule
        promo_code_rule.allowed_brands.add(*brands)

        # Create Conditions Rule
        conditions_list = []
        for condition in conditions:
            conditions_list.append(ConditionRule(operator=condition['operator'], price=condition['price']))

        condition_rules = ConditionRule.objects.bulk_create(conditions_list)

        # Set Conditions
        promo_code_rule.conditions.add(*condition_rules)

        return promo_code

    def create_promo_codes(self, quantity, type, value, valid_until=None, prefix=""):
        promo_codes = []
        for i in range(quantity):
            promo_code.append(self.create_coupon(type, value, None, valid_until, prefix))
        return promo_codes

    def expired(self):
        return self.filter(rules__validity__valid_until__lt=timezone.now())


class PromoCode(models.Model):

    code = models.CharField(max_length=30, unique=True, blank=True,
        help_text=("Leaving this field empty will generate a random code."))

    discount_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='promo_code')
    discount_object_id = models.PositiveIntegerField()
    discount_object = GenericForeignKey('discount_type', 'discount_object_id')

    created_at = models.DateTimeField(auto_now_add=True)

    objects = PromoCodeManager()

    class Meta:
        ordering = ['created_at']
        verbose_name = ("PromoCode")
        verbose_name_plural = ("Promo Codes")

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = PromoCode.generate_code()
        super(PromoCode, self).save(*args, **kwargs)

    @property
    def is_active(self):
        return self.rules.validity.is_active

    @property
    def activate(self):
        return self.rules.validity.activate

    @property
    def is_started(self):
        return self.rules.validity.is_started

    @property
    def is_expired(self):
        return self.rules.validity.is_expired

    @property
    def is_valid(self):
        return self.rules.validity.is_valid

    @property
    def is_limit_reached(self):
        return self.rules.usage.is_limit_reached

    def is_user_limit_reached(self, user):
        return self.rules.usage.is_user_limit_reached(user)

    def is_eligible_for_user(self, user):
        return self.rules.allowed_users.is_eligible_for_user(user)

    @property
    def get_eligible_users(self):
        return self.rules.allowed_users.get_eligible_users

    def redeem(self, user):

        if self.is_limit_reached() or self.is_user_limit_reached(user):
            return False

        redemption = Redemption.objects.create(user=user, promo_code=self)
        if not redemption:
            return False

        self.rules.usage.increase_number_of_uses()
        return True

    def check_conditions(self, order_amount=0):

        if not order_amount:
            return False

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

    @classmethod
    def generate_code(cls, prefix="", segmented=SEGMENTED_CODES):
        code = "".join(random.choice(CODE_CHARS) for i in range(CODE_LENGTH))
        if segmented:
            code = SEGMENT_SEPARATOR.join([code[i:i + SEGMENT_LENGTH] for i in range(0, len(code), SEGMENT_LENGTH)])
            return prefix + code
        else:
            return prefix + code

class ConditionRule(models.Model):
    operator = models.CharField(max_length=1)
    price = MoneyField(max_digits=14, decimal_places=4, default=10,
        validators=[
        MinMoneyValidator(1)
        ], default_currency='SAR')


class AllowedUsersRule(models.Model):
    users = models.ManyToManyField(User, verbose_name="Users", blank=True)
    all_users = models.BooleanField(default=False, verbose_name="All users?")

    class Meta:
        verbose_name = "Allowed User Rule"
        verbose_name_plural = "Allowed User Rules"

    def __str__(self):
        return "AllowedUsersRule Nº{0}".format(self.id)

    def is_eligible_for_user(self, user):
        return user in self.users.all() or self.all_users

    def get_eligible_users(self):
        return self.users.all()



class UsageRule(models.Model):
    max_uses = models.BigIntegerField(default=1, verbose_name="Maximum uses")
    is_infinite = models.BooleanField(default=False, verbose_name="Infinite uses?")
    usage_limit_per_user = models.PositiveIntegerField(default=1, verbose_name="Uses per user")
    user_usage_is_infinite = models.BooleanField(default=False, verbose_name="Infinite uses per user?")
    number_of_uses = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Usage Rule"
        verbose_name_plural = "Usage Rules"

    def __str__(self):
        return "UsageRule Nº{0}".format(self.id)

    @property
    def is_limit_reached(self):
        return self.number_of_uses >= self.max_uses and not self.is_infinite

    def is_user_limit_reached(self, user):
        if not self.parent_rule.first().allowed_users.is_eligible_for_user(user):
            return None

        return self.parent_rule.first().promo_code.redemptions.filter(user=user).count() >= self.usage_limit_per_user and not self.user_usage_is_infinite

    def increase_number_of_uses(self):
        self.number_of_uses = F('number_of_uses') + 1
        self.save(update_fields=['number_of_uses'])

    def decrease_number_of_uses(self):
        self.number_of_uses = F('number_of_uses') - 1
        self.save(update_fields=['number_of_uses'])



class ValidityRule(models.Model):
    valid_from = models.DateField(default=date.today, verbose_name="Valid from date")
    valid_until = models.DateField(default=date.today, verbose_name="Expiration date")
    is_active = models.BooleanField(default=True, verbose_name="Is active?")

    class Meta:
        verbose_name = "Validity Rule"
        verbose_name_plural = "Validity Rules"

    def __str__(self):
        return "ValidityRule Nº{0}".format(self.id)

    @property
    def is_started(self):
        return self.valid_from <= date.today()

    @property
    def is_expired(self):
        return self.valid_until < date.today()

    @property
    def is_valid(self):
        return self.is_started and self.is_active and not self.is_expired

    @property
    def activate(self):
        self.is_active = True
        self.save()
        return True

class PromoCodeRule(models.Model):
    promo_code = models.OneToOneField(PromoCode, on_delete=models.CASCADE, related_name='rules')
    allowed_categories = models.ManyToManyField(Category, blank=True, help_text = "If set to Null, it means general.")
    allowed_brands = models.ManyToManyField(Brand, blank=True, help_text = "If set to Null, it means general.")
    allowed_users = models.ForeignKey(AllowedUsersRule, on_delete=models.CASCADE, verbose_name="Allowed users rule", related_name='parent_rule')
    usage = models.ForeignKey(UsageRule, on_delete=models.CASCADE, verbose_name="Max uses rule", related_name='parent_rule')
    validity = models.ForeignKey(ValidityRule, on_delete=models.CASCADE, verbose_name="Validity rule", related_name='parent_rule')
    conditions = models.ManyToManyField(ConditionRule, blank=True, help_text = "If set to Null, it means general.")

    def __str__(self):
        return f'{self.promo_code.code} Rules'

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

class Redemption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='redemptions')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name='redemptions')
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
