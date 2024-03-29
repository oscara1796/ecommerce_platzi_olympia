# Generated by Django 3.1.6 on 2021-03-03 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_auto_20210302_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_payment_intent',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='payment intent stripe'),
        ),
        migrations.AlterField(
            model_name='userpaymentmethodsstripe',
            name='stripe_payment_id',
            field=models.CharField(max_length=100, verbose_name='stripe payment id'),
        ),
    ]
