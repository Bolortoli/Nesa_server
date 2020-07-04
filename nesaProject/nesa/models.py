from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator


class ServerCategory(models.Model):
    name=models.CharField(max_length=254, verbose_name="Server-ийн төрөл")
    pic=models.ImageField(upload_to='servers/category', verbose_name="Server-ийн төрлийн зураг")

    def __str__(self):
        return self.name

class ActiveServers(models.Model):

    SERVER_CHOICES = [
        ('PREMIUM', 'Premium'),
        ('NON PREMIUM', 'Non premium')
    ]

    name=models.CharField(max_length=254, verbose_name="Server-ийн нэр")
    pic=models.ImageField(verbose_name="Server-ийн зураг", upload_to="servers")
    category=models.ForeignKey(ServerCategory, verbose_name="Category", on_delete=models.CASCADE) 
    server_type=models.CharField(verbose_name="Төлбөртэй эсэх", choices=SERVER_CHOICES, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="Идэвхтэй server - Жагсаалт"
        verbose_name="Идэвхтэй server"

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

# Current date
def current_year():
    return datetime.date.today().year

def current_month():
    return datetime.date.today().month

class Reward(models.Model):
    # Server name
    serName=models.OneToOneField(ActiveServers, on_delete=models.CASCADE)
    pic=models.ImageField(verbose_name="Шагналын зураг", upload_to="rewards")
    year=models.IntegerField(default=current_year(), validators=[MinValueValidator(current_year()), MaxValueValidator(current_year() + 10)])
    month=models.IntegerField(default=current_month() + 1, validators=[MinValueValidator(1), MaxValueValidator(12)])

    class Meta:
        verbose_name_plural="Шагнал- Жагсаалт"
        verbose_name="Шагнал"

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
    logo=models.ImageField(upload_to="settings", verbose_name="Сайтын лого", default="")

    # PROMOTIONS in home page
    # Box-1
    box1_title=models.CharField(max_length=255,verbose_name="Box 1-Гарчиг", blank=True)
    box1_text=models.CharField(max_length=255, verbose_name="Box 1-Текст", blank=True)
    # box1_pic=models.ImageField(upload_to="settings", verbose_name="Box 1-Зураг", default="", blank=True)

    # Box-2
    box2_title=models.CharField(max_length=255, verbose_name="Box 2-Гарчиг", blank=True)
    box2_text=models.CharField(max_length=255, verbose_name="Box 2-Текст", blank=True)
    # box2_pic=models.ImageField(upload_to="settings", verbose_name="Box 2-Зураг", default="", blank=True)

    # Box-3
    box3_title=models.CharField(max_length=255, verbose_name="Box 3-Гарчиг", blank=True)
    box3_text=models.CharField(max_length=255, verbose_name="Box 3-Текст", blank=True)
    #box3_pic=models.ImageField(upload_to="settings", verbose_name="Box 3-Зураг", default="", blank=True)
    
    # Box-4
    box4_title=models.CharField(max_length=255, verbose_name="Box 4-Гарчиг", blank=True)
    # box4_text=models.CharField(max_length=255, verbose_name="Box 4-Текст", blank=True)
    # box4_pic=models.ImageField(upload_to="settings", verbose_name="Box 4-Зураг", default="", blank=True)
    
    # Phone number
    phone_no=models.CharField(max_length=255, verbose_name="Холбоо барих утасны дугаар", default="")

    # Guide video
    guide_vid=models.FileField(upload_to="settings/videos",verbose_name="Заавар бичлэг",
                                validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'wmv', 'qt', 'mov'])], blank=True, default=None)
    def __str__(self):
        return self.title

    class Meta: 
        verbose_name="Вэб Сайтын Тохиргоо"
    