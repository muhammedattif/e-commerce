# Generated by Django 4.0.1 on 2022-02-01 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='final_price',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='final_price_currency',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='final_price',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='final_price_currency',
        ),
    ]