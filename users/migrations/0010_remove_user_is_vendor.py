# Generated by Django 4.0.1 on 2022-04-29 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_vendor',
        ),
    ]