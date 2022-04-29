# Generated by Django 4.0.1 on 2022-04-29 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_is_vendor_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_vendor',
            field=models.BooleanField(default=False, verbose_name='Vendor status'),
        ),
        migrations.DeleteModel(
            name='vendor',
        ),
    ]
