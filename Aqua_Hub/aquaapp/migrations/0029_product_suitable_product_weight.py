# Generated by Django 5.1 on 2025-01-22 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquaapp', '0028_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='suitable',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
