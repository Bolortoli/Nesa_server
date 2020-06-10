from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home.html', {'name' : 'Bolortoli'})

def rewards(request):
    return render(request, 'rewards.html', {'name' : 'Bolortoli'})

def contactUs(request):
    return render(request, 'contactUs.html', {'name' : 'Bolortoli'})
