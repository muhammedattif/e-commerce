# Generated by Django 4.0.1 on 2022-04-23 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_feature_options_alter_featureoption_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='products',
            field=models.ManyToManyField(blank=True, to='products.Product', verbose_name='Product'),
        ),
    ]
