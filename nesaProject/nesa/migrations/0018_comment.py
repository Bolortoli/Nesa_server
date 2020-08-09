# Generated by Django 3.0.7 on 2020-08-07 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nesa', '0017_auto_20200801_0246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default='', max_length=255, verbose_name='Холбогдох мэдээ')),
                ('name', models.CharField(default='', max_length=255, verbose_name='Нэр')),
                ('pic_url', models.CharField(default='', max_length=255, verbose_name='Зураг')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(default='', verbose_name='Сэтгэгдэл')),
            ],
            options={
                'verbose_name': 'Сэтгэгдэл',
                'verbose_name_plural': 'Сэтгэгдэл',
            },
        ),
    ]