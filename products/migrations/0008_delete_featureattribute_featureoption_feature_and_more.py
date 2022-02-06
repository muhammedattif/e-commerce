# Generated by Django 4.0.1 on 2022-02-06 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_remove_stock_attributes_stock_options'),
        ('products', '0007_featureoption_alter_featureattribute_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FeatureAttribute',
        ),
        migrations.AddField(
            model_name='featureoption',
            name='feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='products.feature'),
        ),
        migrations.AlterUniqueTogether(
            name='featureoption',
            unique_together={('feature', 'name')},
        ),
    ]