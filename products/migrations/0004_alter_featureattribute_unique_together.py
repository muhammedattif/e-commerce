# Generated by Django 4.0.1 on 2022-02-01 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_feature_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='featureattribute',
            unique_together={('feature', 'name')},
        ),
    ]