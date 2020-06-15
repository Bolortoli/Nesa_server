from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# Active servers
class ActiveServers(models.Model):
    name=models.CharField(max_length=254, verbose_name="Server-ийн нэр")
    pic=models.ImageField(verbose_name="Server-ийн зураг", upload_to="servers")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="Идэвхтэй server - Жагсаалт"
        verbose_name="Идэвхтэй server"

# Contact us 
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
# Reward
class Reward(models.Model):
    serName=models.OneToOneField(ActiveServers, on_delete=models.CASCADE)
    pic=models.ImageField(verbose_name="Шагналын зураг", upload_to="rewards")
    year=models.IntegerField(default=current_year(), validators=[MinValueValidator(current_year()), MaxValueValidator(current_year() + 10)])
    month=models.IntegerField(default=current_month(), validators=[MinValueValidator(1), MaxValueValidator(12)])


# Global page settings
class Settings(models.Model):
    title=models.CharField(max_length=250,default='Сайтын Тохиргоо',editable=False)

    # Social Media
    facebook=models.URLField(max_length=200,default='',blank=True,verbose_name="Фэйсбоок")
    twitter=models.URLField(max_length=200,default='',blank=True,verbose_name="Твиттер")
    gmail=models.URLField(max_length=200,default='',blank=True,verbose_name="Цахим Хаяг")
    steam=models.URLField(max_length=200,default='',blank=True,verbose_name="Цахим Хаяг")
    youtube=models.URLField(max_length=200,default='',blank=True,verbose_name="Цахим Хаяг")
    twitch=models.URLField(max_length=200,default='',blank=True,verbose_name="Цахим Хаяг")
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="Вэб Сайтын Тохиргоо"
        verbose_name="Вэб Сайтын Тохиргоо"
    