# Generated by Django 5.1.5 on 2025-01-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_sale',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
