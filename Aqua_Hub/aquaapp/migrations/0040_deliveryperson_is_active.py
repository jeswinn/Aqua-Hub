# Generated by Django 5.1 on 2025-03-11 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquaapp', '0039_deliveryperson_address_deliveryperson_pin_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryperson',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
