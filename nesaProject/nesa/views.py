from django.shortcuts import render
from .models import ContactUs

# Create your views here.
def index(req):
    return render(req, 'home.html')               

def contactUs(req):
    if req.method == 'POST':
        item = ContactUs(fullName=req.POST['name'],email=req.POST['email']
            ,phone=req.POST['phone'],text=req.POST['text'])
        item.save()
    return render(req, 'contactUs.html')

def rewardsBlogArchive(req):
    return render(req, 'rewards-blog-archive.html')   

def newsBlogArchive(req):
    return render(req, 'news-blog-archive.html')

def rewardsBlogSingle(req):
    return render(req, 'rewards-blog-single.html')

def newsBlogSingle(req):
    return render(req, 'news-blog-single.html')    

def rewardsBlogGrid(req):
    return render(req,'rewards-blog-grid.html')
