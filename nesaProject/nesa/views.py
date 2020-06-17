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
def blogGrid(req):
    return render(req, 'blogGrid.html')   

def blogSingle(req):
    return render(req, 'blogSingle1.html')
