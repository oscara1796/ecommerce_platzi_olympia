# Generated by Django 3.1.6 on 2021-03-02 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0022_auto_20210302_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpaymentmethodsstripe',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]