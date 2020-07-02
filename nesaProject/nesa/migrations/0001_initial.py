# Generated by Django 3.0.7 on 2020-07-02 08:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveServers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Server-ийн нэр')),
                ('pic', models.ImageField(upload_to='servers', verbose_name='Server-ийн зураг')),
            ],
            options={
                'verbose_name': 'Идэвхтэй server',
                'verbose_name_plural': 'Идэвхтэй server - Жагсаалт',
            },
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=254, verbose_name='Бүтэн Нэр')),
                ('email', models.EmailField(max_length=254, verbose_name='Эмайл Хаяг')),
                ('phone', models.CharField(max_length=12, verbose_name='Утас')),
                ('text', models.TextField(verbose_name='Агуулга')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Бидэнтэй Холбогдох',
                'verbose_name_plural': 'Бидэнтэй Холбогдох - Хүсэлтүүд',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Сайтын Тохиргоо', editable=False, max_length=250)),
                ('facebook', models.URLField(blank=True, default='', verbose_name='Фэйсбоок')),
                ('twitter', models.URLField(blank=True, default='', verbose_name='Твиттер')),
                ('gmail', models.URLField(blank=True, default='', verbose_name='Gmail хаяг')),
                ('steam', models.URLField(blank=True, default='', verbose_name='Steam хаяг')),
                ('youtube', models.URLField(blank=True, default='', verbose_name='Youtube хаяг')),
                ('twitch', models.URLField(blank=True, default='', verbose_name='Twitch хаяг ')),
                ('logo', models.ImageField(default='', upload_to='settings', verbose_name='Сайтын лого')),
                ('box1_title', models.CharField(blank=True, max_length=255, verbose_name='Box 1-Гарчиг')),
                ('box1_text', models.CharField(blank=True, max_length=255, verbose_name='Box 1-Текст')),
                ('box1_pic', models.ImageField(blank=True, default='', upload_to='settings', verbose_name='Box 1-Зураг')),
                ('box2_title', models.CharField(blank=True, max_length=255, verbose_name='Box 2-Гарчиг')),
                ('box2_text', models.CharField(blank=True, max_length=255, verbose_name='Box 2-Текст')),
                ('box2_pic', models.ImageField(blank=True, default='', upload_to='settings', verbose_name='Box 2-Зураг')),
                ('box3_title', models.CharField(blank=True, max_length=255, verbose_name='Box 3-Гарчиг')),
                ('box3_text', models.CharField(blank=True, max_length=255, verbose_name='Box 3-Текст')),
                ('box3_pic', models.ImageField(blank=True, default='', upload_to='settings', verbose_name='Box 3-Зураг')),
                ('box4_title', models.CharField(blank=True, max_length=255, verbose_name='Box 4-Гарчиг')),
                ('box4_text', models.CharField(blank=True, max_length=255, verbose_name='Box 4-Текст')),
                ('box4_pic', models.ImageField(blank=True, default='', upload_to='settings', verbose_name='Box 4-Зураг')),
                ('phone_no', models.CharField(blank=True, default='', max_length=255, verbose_name='Холбоо барих утасны дугаар')),
                ('guide_vid', models.FileField(default=None, upload_to='settings/videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'wmv', 'qt', 'mov'])], verbose_name='Заавар бичлэг')),
            ],
            options={
                'verbose_name': 'Вэб Сайтын Тохиргоо',
                'verbose_name_plural': 'Вэб Сайтын Тохиргоо',
            },
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='rewards', verbose_name='Шагналын зураг')),
                ('year', models.IntegerField(default=2020, validators=[django.core.validators.MinValueValidator(2020), django.core.validators.MaxValueValidator(2030)])),
                ('month', models.IntegerField(default=8, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('serName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nesa.ActiveServers')),
            ],
        ),
    ]
