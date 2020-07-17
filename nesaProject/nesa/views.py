from django.shortcuts import render
from .models import *
import datetime
from django.utils.text import slugify

# Upcoming rewards length to show on upcoming events
UPCOMING_REWARDS_COUNT = 3
ONLY_ONE_REWARD_IN_QUERY = 1

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
    upcoming_events = get_upcoming_events()

    context = {
        'servers': obj_list,
        'single_premium_server': single_prem_srv,
        'single_non_premium_server': single_non_prem_srv,
        'upcoming_events': upcoming_events
    }
    return render(req, 'rewards-blog-archive.html', context)   

def newsBlogArchive(req):
    news_list = News.objects.all()

    context = {
        'news_list': news_list
    }

    return render(req, 'news-blog-archive.html', context)

def rewardsBlogSingle_by_slug(req, slug):
    
    upcoming_events = get_upcoming_events(slug)       
    paid_server_list = ActiveServers.objects.filter(server_type="Premium")
    obj_list = Reward.objects.get(slug=slug)
    context = {
            'obj': obj_list,
            'paid_server_list': paid_server_list,
            'upcoming_events': upcoming_events,
            'ex': True
        }
    return render(req, 'rewards-blog-single.html', context)


def get_upcoming_events(slug=None):
    if slug is not None:
        return Reward.objects.all().order_by('-year', '-month').exclude(slug=slug)[:UPCOMING_REWARDS_COUNT] if Reward.objects.count() >= UPCOMING_REWARDS_COUNT else Reward.objects.all()          
    else:
        return Reward.objects.all().order_by('-year', '-month')[:UPCOMING_REWARDS_COUNT] if Reward.objects.count() >= UPCOMING_REWARDS_COUNT else Reward.objects.all()

def rewardsBlogSingle_by_server(req, server):
    year = datetime.date.today().year
    month = datetime.date.today().month 
    
    reward_object = None
    server_rewards_exist = True
    upcoming_events = None

    eslug=slugify(server)+'-'+str(year)+'-'+str(month)
    try:
        reward_object = Reward.objects.get(slug=eslug)
        upcoming_events = get_upcoming_events(eslug)          

    except:
        reward_object = Reward.objects.filter(serName__name=server)

        # Check if table has only one record
        if reward_object.count() == ONLY_ONE_REWARD_IN_QUERY:
            reward_object = reward_object.first()
            upcoming_events = get_upcoming_events(reward_object.slug)

        # Check if table has no record
        elif reward_object.count() == 0:
            reward_object = None
            server_rewards_exist = False
            upcoming_events = get_upcoming_events()

        # Else return latest reward
        else:
            reward_object = reward_object.order_by('year', 'month').first()
            upcoming_events = get_upcoming_events(reward_object.slug)


    paid_server_list = ActiveServers.objects.filter(server_type="Premium").exclude(name=server)

    # server_objects = Reward.objects.filter(serName__name=server).order_by('-year', '-month')
    # c = Reward.objects.filter(serName__name='nesa.mn:27018').count()

    context = {
        'obj': reward_object,
        'paid_server_list': paid_server_list,
        'upcoming_events': upcoming_events,
        # 'count': server_objects,
        # 'c': c,
        'ex': server_rewards_exist
    }
    return render(req, 'rewards-blog-single.html', context)


def newsBlogSingle(req):
    return render(req, 'news-blog-single.html')        

def rewardsBlogGrid(req):
    rewards = Reward.objects.all()
    upcoming_events = get_upcoming_events()   

    context = {
        'rewards': rewards,
        'upcoming_events': upcoming_events
    }
    return render(req,'rewards-blog-grid.html', context)

def logindex(req):
    return render(req,'logindex.html')
