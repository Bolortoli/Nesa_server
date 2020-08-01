from django.views.decorators.csrf import csrf_exempt
from .models import *
import uuid, datetime, requests, json, calendar
from django.utils.text import slugify
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# from django.views.generic.base import TemplateView
from datetime import datetime as dt
from datetime import timedelta  
from django.core.paginator import Paginator 

UPCOMING_REWARDS_COUNT = 3
ONLY_ONE_REWARD_IN_QUERY = 1
REWARDS_COUNT_IN_HOME = 5
QR_PICS_COUNT = 3
MERCHANT_ID = "TEST_MERCHANT"
QPAY_CHECK_URL_POST = "https://api.qpay.mn/v1/in_store/check"
PAYMENT_PER_MONTH = 0.99
PAYMENT_PERIOD_DAYS_PER_MONTH = 30


def index(req):

    if req.user.is_authenticated:

        qlist = []

        get_access_token(req)

        register_user(req)

        create_temp_id(req)

        register_payment(req)

        for i in range(QR_PICS_COUNT):
            # bill = uuid.uuid4()
            response = requests.post("https://api.qpay.mn/v1/bill/create",json={
                "template_id": "TEST_INVOICE",
                "merchant_id": MERCHANT_ID,
                "branch_id": "1",
                "pos_id": "1",
                "receiver": {
                    "id": "CUST_001",
                    "register_no": "ddf",
                    "name": "Central brnach",
                    "email": "info@info.mn",
                    "phone_number":"99888899",
                    "note" : str(req.user.personaname) + '-ийн ' + str(int(i + 1)) + ' сарын төлбөр',
                },
                "bill_no": str(TempPaymentId.objects.get(name=req.user.personaname, month=i+1).bill_no),
                "date": str(datetime.date.today()),
                "description":str(req.user.personaname) + '-ийн ' + str(int(i + 1)) + ' сарын төлбөр',
                "amount": str((int(i + 1))),
                "btuk_code":"",     
                "vat_flag": "0",
            }, headers={
                'Content-Type' : 'application/json',
                'Authorization' : 'Bearer ' + req.session['access_token']
            })
            resp_data = response.json() 
            qlist.append(QRObject(resp_data, str((int(i + 1))*1000), int(i + 1)))
  
        reward_list = get_rewards(count=REWARDS_COUNT_IN_HOME)
        
        news_list = News.objects.all()
        contact_request(req)

        context = {
            'reward_list': reward_list,
            'news_list': news_list,
            'qlist': qlist,
            # 'check': check,

        }

    else :
        reward_list = get_rewards(count=REWARDS_COUNT_IN_HOME)
        news_list = News.objects.all()
        contact_request(req)
        context = {
            'reward_list': reward_list,
            'news_list': news_list
        }
    print('before return html')
    return render(req, 'home.html', context)               

def contactUs(req):
    contact_request(req)
    return render(req, 'contactUs.html')

@csrf_exempt
def kk(request):
    register_payment(request)
    generate_whitelist(request)
    create_temp_id(request)
    print("kk")

    return JsonResponse({'tr': Whitelist.objects.get(steamid=request.user.steamid).expDate})

def rewardsBlogArchive(req):
    obj_list = ActiveServers.objects.all()

    single_prem_srv = premium_obj(obj_list=obj_list)
    single_non_prem_srv = non_premium_obj(obj_list=obj_list)
    upcoming_events = get_rewards(count=UPCOMING_REWARDS_COUNT)
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
        'object': single_news,
        'news': single_news,
    }

    return render(req, 'news-blog-single.html', context)        

def rewardsBlogGrid(req):
    obj_list = Reward.objects.all()

    paginator = Paginator(obj_list, 6)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    upcoming_events = get_rewards(count=UPCOMING_REWARDS_COUNT)   
    latest_news = get_news(3, True)
    contact_request(req)

    context = {
        'rewards': page_obj,
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
    if not request.user.is_superuser:
        if request.POST.get("form_type") == '':
            item = ContactUs(fullName=request.POST['name'],email=request.POST['email']
                ,phone=request.POST['phone'],text=request.POST['text'])
            item.save() 
    
def get_access_token(request):
    if 'access_token' not in request.session:
        response = requests.post("https://api.qpay.mn/v1/auth/token",json={
            "client_id": "qpay_test",
            "client_secret": "sdZv9k9m",
            "grant_type":"client",
            "refresh_token":""
        }, headers={
            'Content-Type' : 'application/json'
        })
        request.session["access_token"] = response.json()["access_token"]

def register_user(request):
    if not User.objects.filter(steamuser=request.user).exists():
        item = User(email="bo@gmail.com", phone_no="99111111", steamuser=request.user)
        item.save()

def create_temp_id(req):
    if not TempPaymentId.objects.filter(name=req.user.personaname).exists():
        for i in range(QR_PICS_COUNT):
            TempPaymentId(month=(i+1), user=User.objects.get(steamuser=req.user), bill_no=uuid.uuid4().hex).save()      

def get_all_unregistered_payments(req):
    payments = []
    if PaymentHistory.objects.filter(user=User.objects.get(steamuser=req.user), registered=False).exists():
        wegothistory = PaymentHistory.objects.filter(user=User.objects.get(steamuser=req.user)).order_by('created_date')
        for i in wegothistory:
            payments.append(i)
    return payments


def register_payment(req):

    for i in TempPaymentId.objects.filter(name=req.user.personaname):

        payload = "{\n  \"merchant_id\": \"%s\",\n  \"order_no\": \"%s\"\n}" % (MERCHANT_ID, i.bill_no)

        headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Bearer ' + req.session['access_token']
        }

        check = requests.request("POST", QPAY_CHECK_URL_POST, headers=headers, data = payload).json()
        try:
            if check['payment_info']['payment_status'] == "PAID":
                print("checkcheck")
                i.bill_no = str(uuid.uuid4().hex)
                i.save()
                PaymentHistory(user=User.objects.get(steamuser=req.user), data=(json.dumps(check)), registered=True).save()
        except KeyError:
            continue


def split_date(date):
    date = date.split()
    print("asdqwerty")
    print(date)
    period = date[0].split('-')
    time = date[1].split(':')

    return dt(year=int(period[0]), month=int(period[1]), day=int(period[2]), hour=int(time[0]), minute=int(time[1]), second=int(time[2]))


def generate_and_save(request):
    payments_unregistered = get_all_unregistered_payments(request)
    whitelist = Whitelist.objects.get(steamid=request.user.steamid)
    for i in payments_unregistered:

        json_data = json.loads(i.data)
        paid_date = json_data["payment_info"]["transactions"][0]["transaction_date"]
        amount = json_data["payment_info"]["transactions"][0]["transaction_amount"]
        print(paid_date)
        payment_month = int(float(amount)/PAYMENT_PER_MONTH)
        # print(payment_month)
        if not whitelist.expDate:
            date = split_date(str(paid_date))
            print(date)
        else:
            date = split_date(str(paid_date)) if whitelist.is_expired() else split_date(str(whitelist.expDate))

        exp_date = date + timedelta(days=payment_month*PAYMENT_PERIOD_DAYS_PER_MONTH)
        whitelist.expDate = str(exp_date)
        whitelist.save()
        i.registered = True
        i.save()

def generate_whitelist(request):
    p = None
    payments_unregistered = get_all_unregistered_payments(request)

    if payments_unregistered: 
        if not Whitelist.objects.filter(steamid=request.user.steamid).exists():
            Whitelist(steamid=request.user.steamid, phone_no=User.objects.get(steamuser=request.user).phone_no, email=User.objects.get(steamuser=request.user).email).save()
            generate_and_save(request)
        else:
            generate_and_save(request)
    else:
        if not Whitelist.objects.filter(steamid=request.user.steamid).exists():
            Whitelist(steamid=request.user.steamid, phone_no=User.objects.get(steamuser=request.user).phone_no, email=User.objects.get(steamuser=request.user).email).save()
        


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('auth:index')

class QRObject:
    def __init__(self, resp_data, amount, month):
        self.qpay_qr = resp_data['qPay_url']
        self.amount = amount
        self.month = month
