# Generated by Django 3.1.6 on 2021-02-25 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='porcentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Descuento'),
        ),
    ]
