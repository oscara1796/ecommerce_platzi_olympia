# Generated by Django 3.1.6 on 2021-02-28 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_coupon_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='user',
        ),
    ]