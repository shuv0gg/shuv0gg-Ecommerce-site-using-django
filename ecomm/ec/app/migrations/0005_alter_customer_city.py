# Generated by Django 5.1.4 on 2024-12-14 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(max_length=200),
        ),
    ]
