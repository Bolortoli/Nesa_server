# Generated by Django 3.0.7 on 2020-07-06 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nesa', '0002_auto_20200705_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeservers',
            name='server_type',
            field=models.CharField(choices=[('Premium', 'Premium'), ('Non Premium', 'Non premium')], default=('Premium', 'Premium'), max_length=50, verbose_name='Төлбөртэй эсэх'),
        ),
    ]
