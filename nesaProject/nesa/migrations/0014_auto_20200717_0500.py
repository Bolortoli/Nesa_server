# Generated by Django 3.0.7 on 2020-07-17 05:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('nesa', '0013_auto_20200717_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
