# Generated by Django 3.0.7 on 2020-07-25 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nesa', '0011_paymenthistory_registered'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='created_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
