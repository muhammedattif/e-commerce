# Generated by Django 4.0.1 on 2022-01-31 12:40

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_alter_cart_discount_alter_cart_sub_total_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='sub_total',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=4, default=Decimal('0'), max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=4, default=Decimal('0'), max_digits=14, null=True),
        ),
    ]