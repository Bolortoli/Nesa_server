from django.db import models
import datetime
import math
import uuid
import itertools
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.utils.text import slugify
from django.contrib.auth.models import User
from random import randint
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _ 
from django.utils import timezone
import jsonfield
from datetime import datetime as dt

class ServerCategory(models.Model):
    name=models.CharField(max_length=254, verbose_name="Server-ийн төрөл")
    pic=models.ImageField(upload_to='servers/category', verbose_name="Server-ийн категорийн зураг")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="Серверийн категори"
        verbose_name="Төрөл"

class ActiveServers(models.Model):

    SERVER_CHOICES = [
        ('Premium', 'Premium'),
        ('Non Premium', 'Non premium')
    ]

    name=models.CharField(max_length=254, verbose_name="Server-ийн нэр", unique=True)
    pic=models.ImageField(verbose_name="Server-ийн зураг", upload_to="servers")
    category=models.ForeignKey(ServerCategory, verbose_name="Category", on_delete=models.CASCADE, default='') 
    server_type=models.CharField(verbose_name="Төлбөртэй эсэх", choices=SERVER_CHOICES, max_length=50, default=SERVER_CHOICES[0])

    def get_title_as_slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    def is_premium(self):
        return True if self.server_type == "Premium" else False

    class Meta:
        verbose_name_plural="Идэвхтэй server - Жагсаалт"
        verbose_name="Идэвхтэй server"


# Current date
def current_year():
    return datetime.date.today().year

def current_month():
    return datetime.date.today().month

class Reward(models.Model):
    # Server name
    title=models.CharField(max_length=255, verbose_name="Шагналын гарчиг", default='')
    serName=models.ForeignKey(ActiveServers, on_delete=models.CASCADE)
    pic=models.ImageField(verbose_name="Шагналын зураг", upload_to="rewards")
    year=models.IntegerField(default=current_year(), validators=[MinValueValidator(current_year()), MaxValueValidator(current_year() + 10)])    
    month=models.IntegerField(default=current_month() + 1, validators=[MinValueValidator(1), MaxValueValidator(12)])
    published_date=models.DateField(verbose_name="Огноо", auto_now_add=True, editable=False)
    sponsor_name=models.CharField(max_length=255, verbose_name=" Ивээн тэтгэгч", default='')
    desc=models.TextField(verbose_name="Мэдээний тайлбар", default='')
    slug=models.CharField(max_length=250, unique=True, editable=False, default='')

    def __str__(self):
        return self.serName.name + '-ын шагнал'

    def save(self, *args, **kwargs):
        new_slug = slugify("%s %d %d" % (self.serName.name, self.year, self.month))
        slug_count = 1
        if Reward.objects.filter(slug = new_slug).exists():
            new_slug = slugify("%s %d" % (new_slug, slug_count))            
            for slug_addition_count in itertools.count(slug_count):
                if not Reward.objects.filter(slug = new_slug).exists(): 
                    break
                else: 
                    # Remove last '-' and digit to make a new slug without make a new variable
                    new_slug = new_slug[:-((int(math.log10(slug_addition_count))) + 2)]
                    new_slug = slugify("%s %d" % (new_slug, slug_addition_count))
        self.slug = new_slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Шагнал- Жагсаалт"
        verbose_name="Шагнал" 
        

    # def get_absolute_slug(self):
    #     return reverse()


class ContactUs(models.Model):
    fullName=models.CharField(max_length=254,verbose_name="Бүтэн Нэр")
    email=models.EmailField(verbose_name="Эмайл Хаяг")
    phone=models.CharField(max_length=12,verbose_name="Утас")
    text=models.TextField(verbose_name="Агуулга")
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.fullName

    class Meta:
        ordering =('-created',)
        verbose_name_plural="Бидэнтэй Холбогдох - Хүсэлтүүд"
        verbose_name="Бидэнтэй Холбогдох"

# Web global settings
class Settings(models.Model):
    title=models.CharField(max_length=250,default='Сайтын Тохиргоо',editable=False)

    # Social Media
    facebook=models.URLField(max_length=200,default='',blank=True,verbose_name="Фэйсбоок")
    twitter=models.URLField(max_length=200,default='',blank=True,verbose_name="Твиттер")
    gmail=models.URLField(max_length=200,default='',blank=True,verbose_name="Gmail хаяг")
    steam=models.URLField(max_length=200,default='',blank=True,verbose_name="Steam хаяг")
    youtube=models.URLField(max_length=200,default='',blank=True,verbose_name="Youtube хаяг")
    twitch=models.URLField(max_length=200,default='',blank=True,verbose_name="Twitch хаяг ")
    
    # Web logo
    logo=models.ImageField(upload_to="settings", verbose_name="Сайтын лого", default="", blank=True)

    # PROMOTIONS in home page
    # Box-1
    box1_title=models.TextField(max_length=255,verbose_name="Box 1-Гарчиг", blank=True)
    box1_text=models.TextField(max_length=255, verbose_name="Box 1-Текст", blank=True)
    # box1_pic=models.ImageField(upload_to="settings", verbose_name="Box 1-Зураг", default="", blank=True)

    # Box-2
    box2_title=models.TextField(max_length=255, verbose_name="Box 2-Гарчиг", blank=True)
    box2_text=models.TextField(max_length=255, verbose_name="Box 2-Текст", blank=True)
    # box2_pic=models.ImageField(upload_to="settings", verbose_name="Box 2-Зураг", default="", blank=True)

    # Box-3
    box3_title=models.TextField(max_length=255, verbose_name="Box 3-Гарчиг", blank=True)
    box3_text=models.TextField(max_length=255, verbose_name="Box 3-Текст", blank=True)
    #box3_pic=models.ImageField(upload_to="settings", verbose_name="Box 3-Зураг", default="", blank=True)
    
    # Box-4
    box4_title=models.TextField(max_length=255, verbose_name="Box 4-Гарчиг", blank=True)
    # box4_text=models.CharField(max_length=255, verbose_name="Box 4-Текст", blank=True)
    # box4_pic=models.ImageField(upload_to="settings", verbose_name="Box 4-Зураг", default="", blank=True)
    
    # Phone number
    phone_no=models.CharField(max_length=255, verbose_name="Холбоо барих утасны дугаар", default="", blank=True)

    # Guide video
    guide_vid=models.FileField(upload_to="settings/videos",verbose_name="Заавар бичлэг",
                                validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'wmv', 'qt', 'mov'])], blank=True, default=None)
    def __str__(self):
        return self.title

    class Meta: 
        verbose_name="Вэб Сайтын Тохиргоо"
        verbose_name_plural="Тохиргоо"
    

class NewsCategory(models.Model):
    name=models.CharField(verbose_name='Нэр', max_length=255, default="")

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name="Мэдээний категори"
        verbose_name_plural="Категори"

class News(models.Model):
    id=models.CharField(verbose_name='slug', max_length=255, default="", editable=False, unique=True, primary_key=True)
    title=models.CharField(verbose_name='Нэр', max_length=255, default="")
    desc=models.TextField(verbose_name='Мэдээ', default="")
    pic=models.ImageField(upload_to="news", verbose_name="Зураг", default="")
    created=models.DateTimeField(auto_now_add=True, editable=False)
    slug=models.CharField(verbose_name='slug', max_length=255, default="", editable=False)
    category=models.ForeignKey(NewsCategory, verbose_name="Category", on_delete=models.CASCADE, default='')

    def save(self, *args, **kwargs):

        random_number = randint(1000, 999999999)
        while News.objects.filter(id=random_number).exists():
            random_number = randint(1000, 9999999)
        self.id = random_number

        self.slug = slugify("%s %s" % (self.category.name, str(self.id)))
        super().save(*args, **kwargs)

    class Meta: 
        verbose_name="Мэдээ"
        verbose_name_plural="Мэдээ"
class Comment(models.Model):
    slug = models.CharField(verbose_name="Холбогдох мэдээ", max_length=255, default="")
    name = models.CharField(verbose_name="Нэр", max_length=255, default="")
    pic_url = models.CharField(verbose_name="Зураг", max_length=255, default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    comment = models.TextField(verbose_name="Сэтгэгдэл", default="")
    steamid = models.CharField(verbose_name="Steam ID", max_length=255, default="")

    def __str(self):
        return self.name

    class Meta:
        verbose_name = "Сэтгэгдэл"
        verbose_name_plural = "Сэтгэгдэл"


class SteamUserManager(BaseUserManager):
    def _create_user(self, steamid, password, **extra_fields):
        """
        Creates and saves a User with the given steamid and password.
        """
        try:
            # python social auth provides an empty email param, which cannot be used here
            del extra_fields['email']
        except KeyError:
            pass
        if not steamid:
            raise ValueError('The given steamid must be set')
        user = self.model(steamid=steamid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, steamid, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(steamid, password, **extra_fields)

    def create_superuser(self, steamid, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(steamid, password, **extra_fields)


class SteamUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'steamid'

    steamid = models.CharField(max_length=17, unique=True)
    personaname = models.CharField(max_length=255)
    profileurl = models.CharField(max_length=300)
    avatar = models.CharField(max_length=255)
    avatarmedium = models.CharField(max_length=255)
    avatarfull = models.CharField(max_length=255)

    # Add the other fields that can be retrieved from the Web-API if required

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # e_mail=models.CharField(default="", max_length=255, verbose_name="Нэр", blank=True)
    # phone=models.CharField(default="", max_length=255, verbose_name="Нэр", blank=True)

    objects = SteamUserManager()

    def get_short_name(self):
        return self.personaname

    def get_full_name(self):
        return self.personaname


class User(models.Model):
    steamuser = models.ForeignKey(SteamUser, on_delete=models.CASCADE, verbose_name="Steam хэрэглэгч")
    email = models.CharField(verbose_name="Имэйл", max_length=255, blank=True)
    phone_no = models.CharField(verbose_name="Утасны дугаар", max_length=255, blank=True)
    name = models.CharField(verbose_name="Нэр", default="", max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.steamuser.personaname
        super().save(*args, **kwargs)

    class Meta:
        verbose_name="Хэрэглэгчид"
        verbose_name_plural="Хэрэглэгчид"


class PaymentHistory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Steam хэрэглэгч")
    data = models.TextField(verbose_name="JSON дата")
    # data = jsonfield.JSONField()
    registered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.user

class TempPaymentId(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Steam хэрэглэгч")
    bill_no = models.CharField(max_length=255)
    month = models.IntegerField(default=None)
    name = models.CharField(verbose_name="Нэр", default="", max_length=255)


    def save(self, *args, **kwargs):
        self.name = self.user.steamuser.personaname
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.name

class Whitelist(models.Model):
    steamid = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, blank=True)
    phone_no = models.CharField(max_length=255, blank=True)
    expDate = models.CharField(max_length=255, blank=True)

    def is_expired(self):
        date = self.expDate.split()
        period = date[0].split('-')
        time = date[1].split(':')
        return dt(year=int(period[0]), month=int(period[1]), day=int(period[2]), hour=int(time[0]), minute=int(time[1]), second=int(time[2])) < dt.now()
