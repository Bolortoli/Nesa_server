# Generated by Django 3.0.7 on 2020-07-02 08:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nesa', '0002_remove_settings_guide_vid'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='guide_vid',
            field=models.FileField(default=None, upload_to='settings/videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'wmv', 'qt', 'mov'])], verbose_name='Заавар бичлэг'),
        ),
    ]
