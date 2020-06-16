from django.shortcuts import render
from .models import ContactUs

# Create your views here.
def index(req):
    return render(req, 'home.html')

def rewards(req):
    return render(req, 'rewards.html')

def contactUs(req):
    if req.method == 'POST':
        item = ContactUs(fullName=req.POST['name'],email=req.POST['email']
            ,phone=req.POST['phone'],text=req.POST['text'])
        item.save()

    return render(req, 'contactUs.html')
