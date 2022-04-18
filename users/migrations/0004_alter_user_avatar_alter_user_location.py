# Generated by Django 4.0.1 on 2022-04-18 10:39

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=users.models.get_image_filename, verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=100, verbose_name='Location'),
        ),
    ]
