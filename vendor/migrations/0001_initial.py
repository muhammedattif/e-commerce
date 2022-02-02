# Generated by Django 4.0.1 on 2022-02-02 06:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0005_remove_stock_attributes_remove_stock_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('attributes', models.ManyToManyField(to='products.FeatureAttribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='products.product')),
            ],
        ),
    ]
