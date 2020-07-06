from django.shortcuts import render
from .models import ContactUs, ActiveServers

# Create your views here.
def index(req):
    return render(req, 'home.html')               

def contactUs(req):
    if req.method == 'POST':
        item = ContactUs(fullName=req.POST['name'],email=req.POST['email']
            ,phone=req.POST['phone'],text=req.POST['text'])
        item.save()
    return render(req, 'contactUs.html')

def premium_obj(obj_list):
    for obj in obj_list:
        if obj.is_premium:
            return obj 
        
def non_premium_obj(obj_list):
    for obj in obj_list:
        if obj.is_premium is False:
            return obj 
        

def rewardsBlogArchive(req):
    obj_list = ActiveServers.objects.all()
    single_prem_srv = premium_obj(obj_list=obj_list)
    single_non_prem_srv = non_premium_obj(obj_list=obj_list)

    context = {
        'servers': obj_list,
        'single_premium_server': single_prem_srv,
        'single_non_premium_server': single_non_prem_srv
    }
    return render(req, 'rewards-blog-archive.html', context)   

def newsBlogArchive(req):
    return render(req, 'news-blog-archive.html')

def rewardsBlogSingle(req):
    return render(req, 'rewards-blog-single.html')

def newsBlogSingle(req):
    return render(req, 'news-blog-single.html')        

def rewardsBlogGrid(req):
    return render(req,'rewards-blog-grid.html')
