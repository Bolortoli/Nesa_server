# Generated by Django 3.0.7 on 2020-07-13 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nesa', '0006_auto_20200713_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeservers',
            name='name',
            field=models.CharField(max_length=254, unique=True, verbose_name='Server-ийн нэр'),
        ),
    ]
