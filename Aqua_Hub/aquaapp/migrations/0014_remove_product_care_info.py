# Generated by Django 5.1 on 2024-10-09 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aquaapp', '0013_product_behavior_product_feeding_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='care_info',
        ),
    ]