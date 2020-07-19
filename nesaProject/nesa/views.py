from django.shortcuts import render
from .models import *
import datetime
from django.utils.text import slugify
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

UPCOMING_REWARDS_COUNT = 3
ONLY_ONE_REWARD_IN_QUERY = 1
REWARDS_COUNT_IN_HOME = 5

def index(req):
    reward_list = get_rewards(count=REWARDS_COUNT_IN_HOME)
    news_list = News.objects.all()
    contact_request(req)
    context = {
        'reward_list': reward_list,
        'news_list': news_list
    }
    # if req.method == 'POST':
    #     item = SteamUser(e_mail=req.POST['user_email'],phone=req.POST['user_phone'])
    #     item.save() 

    return render(req, 'home.html', context)               

def contactUs(req):
    contact_request(req)
    return render(req, 'contactUs.html')

def rewardsBlogArchive(req):
    obj_list = ActiveServers.objects.all()
    single_prem_srv = premium_obj(obj_list=obj_list)
    single_non_prem_srv = non_premium_obj(obj_list=obj_list)
    upcoming_events = get_rewards()
    contact_request(req)

    context = {
        'servers': obj_list,
        'single_premium_server': single_prem_srv,
        'single_non_premium_server': single_non_prem_srv,
        'upcoming_events': upcoming_events
    }
    return render(req, 'rewards-blog-archive.html', context)   

def newsBlogArchive(req):
    news_list = News.objects.all()
    category_list = NewsCategory.objects.all()
    contact_request(req)

    context = {
        'news_list': news_list,
        'categories': category_list
    }

    return render(req, 'news-blog-archive.html', context)

def rewardsBlogSingle_by_slug(req, slug):
    
    upcoming_events = get_rewards(specified_slug=slug, count=UPCOMING_REWARDS_COUNT)       
    paid_server_list = ActiveServers.objects.filter(server_type="Premium")
    obj_list = Reward.objects.get(slug=slug)
    contact_request(req)

    context = {
            'obj': obj_list,
            'paid_server_list': paid_server_list,
            'upcoming_events': upcoming_events,
            'ex': True
        }
    return render(req, 'rewards-blog-single.html', context)

def rewardsBlogSingle_by_server(req, server):
    year = datetime.date.today().year
    month = datetime.date.today().month 
    
    reward_object = None
    server_rewards_exist = True
    upcoming_events = None

    eslug=slugify(server)+'-'+str(year)+'-'+str(month)
    try:
        reward_object = Reward.objects.get(slug=eslug)
        upcoming_events = get_rewards(specified_slug=eslug, count=UPCOMING_REWARDS_COUNT)          

    except:
        reward_object = Reward.objects.filter(serName__name=server)

        # Check if table has only one record
        if reward_object.count() == ONLY_ONE_REWARD_IN_QUERY:
            reward_object = reward_object.first()
            upcoming_events = get_rewards(specified_slug=reward_object.slug, count=UPCOMING_REWARDS_COUNT)

        # Check if table has no record
        elif reward_object.count() == 0:
            reward_object = None
            server_rewards_exist = False
            upcoming_events = None

        # Else return latest reward
        else:
            reward_object = reward_object.order_by('year', 'month').first()
            upcoming_events = get_rewards(specified_slug=reward_object.slug, count=UPCOMING_REWARDS_COUNT)


    paid_server_list = ActiveServers.objects.filter(server_type="Premium").exclude(name=server)
    contact_request(req)

    context = {
        'obj': reward_object,
        'paid_server_list': paid_server_list,
        'upcoming_events': upcoming_events,
        'ex': server_rewards_exist
    }
    return render(req, 'rewards-blog-single.html', context)


def newsBlogSingle(req, slug):
    single_news = News.objects.get(slug=slug)
    contact_request(req)

    context = {
        'object': single_news
    }

    return render(req, 'news-blog-single.html')        

def rewardsBlogGrid(req):
    rewards = Reward.objects.all()
    upcoming_events = get_rewards(count=UPCOMING_REWARDS_COUNT)   
    latest_news = get_news(3, True)
    contact_request(req)

    context = {
        'rewards': rewards,
        'upcoming_events': upcoming_events,
        'latest_news': latest_news,
    }
    return render(req,'rewards-blog-grid.html', context)

def logindex(req):
    return render(req,'logindex.html')

# FUNCTIONS

def get_rewards(specified_slug=None, count=0):
    if specified_slug is not None and count != 0:
        return Reward.objects.all().order_by('-year', '-month').exclude(slug=specified_slug)[:count] if Reward.objects.count() >= count else Reward.objects.all()  
    # elif specified_slug is None and count != 0:
    else:
        return Reward.objects.all().order_by('-year', '-month')[:count] if Reward.objects.count() >= count else Reward.objects.all()

def get_news(count=0, latest=None):
    # Means no order
    if latest is None:
        return News.objects.all()[:count] if News.objects.count() >= count else News.objects.all()  
    # Means latest in date
    elif latest is True:
        return News.objects.all().order_by('-created')[:count] if News.objects.count() >= count else News.objects.all()
    # Means oldest in date
    elif latest is not True:
        return News.objects.all().order_by('created')[:count] if News.objects.count() >= count else News.objects.all()


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
        
# Get contact request
def contact_request(request):
    if request.method == 'POST':
        item = ContactUs(fullName=request.POST['name'],email=request.POST['email']
            ,phone=request.POST['phone'],text=request.POST['text'])
        item.save() 


# class MyView(View):
#     http_method_names = ['get', 'post']
#     def post(self, request):
#         item = ContactUs(fullName=request.POST['name'],email=request.POST['email']
#             ,phone=request.POST['phone'],text=request.POST['text'])
#         item.save()

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('auth:index')

