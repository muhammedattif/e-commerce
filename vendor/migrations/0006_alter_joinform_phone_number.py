# Generated by Django 4.0.1 on 2022-05-30 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_joinform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinform',
            name='phone_number',
            field=models.CharField(max_length=100, unique=True, verbose_name='Phone Number'),
        ),
    ]
