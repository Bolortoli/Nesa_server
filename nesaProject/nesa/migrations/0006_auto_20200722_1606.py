# Generated by Django 3.0.7 on 2020-07-22 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nesa', '0005_auto_20200722_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=255, verbose_name='Имэйл'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.CharField(blank=True, max_length=255, verbose_name='Утасны дугаар'),
        ),
    ]
