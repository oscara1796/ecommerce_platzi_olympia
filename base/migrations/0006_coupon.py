# Generated by Django 3.1.6 on 2021-02-25 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20210218_2019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre de cupon')),
                ('code', models.CharField(blank=True, max_length=200, null=True, verbose_name='Código')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Descuento')),
                ('active', models.BooleanField(default=False, verbose_name='Activo')),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Cupon',
                'verbose_name_plural': 'Cupones',
                'ordering': ['_id'],
            },
        ),
    ]