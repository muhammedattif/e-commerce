# Generated by Django 4.0.1 on 2022-02-06 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendorprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomerProfile',
        ),
        migrations.DeleteModel(
            name='VendorProfile',
        ),
    ]
