from .models import Settings, News, ContactUs

SPECIAL_NEWS_COUNT = 2

def global_settings(request):
    return {
        'global_settings': Settings.objects.all()[0] if Settings.objects.count() > 0 else Settings.objects.all(),
        'featured_news': News.objects.all().order_by('-created')[:SPECIAL_NEWS_COUNT] if News.objects.count() >=SPECIAL_NEWS_COUNT else News.objects.all()
    }

   