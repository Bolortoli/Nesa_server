from django.shortcuts import render
from .models import ContactUs, ActiveServers, Reward
import datetime
from django.utils.text import slugify


# Create your views here.
def index(req):
    return render(req, 'home.html')               

def contactUs(req):
    if req.method == 'POST':
        item = ContactUs(fullName=req.POST['name'],email=req.POST['email']
            ,phone=req.POST['phone'],text=req.POST['text'])
        item.save()
    return render(req, 'contactUs.html')

# Get single premium server object
def premium_obj(obj_list):
    for obj in obj_list:
        if obj.is_premium():
            return obj 

# Get single premium server object
def non_premium_obj(obj_list):
    for obj in obj_list:
        if obj.is_premium() is not True:
            return obj 
        

def rewardsBlogArchive(req):
    obj_list = ActiveServers.objects.all()
    single_prem_srv = premium_obj(obj_list=obj_list)
    single_non_prem_srv = non_premium_obj(obj_list=obj_list)
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year

    context = {
        'servers': obj_list,
        'single_premium_server': single_prem_srv,
        'single_non_premium_server': single_non_prem_srv,
        'current_month': current_month,
        'current_year': current_year,
    }
    return render(req, 'rewards-blog-archive.html', context)   

def newsBlogArchive(req):
    return render(req, 'news-blog-archive.html')

def rewardsBlogSingle(req, server, year=datetime.date.today().year, month=datetime.date.today().month):
    # eslug=server+'-'+year+'-'+month
    # obj_list = Reward.objects.filter(slug=eslug )

    # TEST CASE

    # server = 'nesamn27019'
    # year = 2020
    # month = 8

    eslug=slugify(server)+'-'+str(year)+'-'+str(month)
    obj_list = Reward.objects.get(slug=eslug)

    paid_server_list = ActiveServers.objects.filter(server_type="Premium")

    context = {
        'obj': obj_list,
        'paid_server_list': paid_server_list,
    }
    return render(req, 'rewards-blog-single.html', context)

def newsBlogSingle(req):
    return render(req, 'news-blog-single.html')        

def rewardsBlogGrid(req):
    return render(req,'rewards-blog-grid.html')

def logindex(req):
    return render(req,'logindex.html')