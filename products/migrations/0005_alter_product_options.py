# Generated by Django 4.0.1 on 2022-01-29 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-creation',)},
        ),
    ]
