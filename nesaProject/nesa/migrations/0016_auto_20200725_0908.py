# Generated by Django 3.0.7 on 2020-07-25 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nesa', '0015_auto_20200725_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='data',
            field=models.TextField(verbose_name='JSON дата'),
        ),
    ]